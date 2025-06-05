<template>
    <div
      style="position:relative; width:640px; height:384px; background:#222; border-radius:12px; overflow:hidden;">
      <video
        ref="video"
        width="640" height="384"
        autoplay
        muted
        playsinline
        style="position:absolute; top:0; left:0; width:640px; height:384px; z-index:1; background:#111;"
      ></video>
      <canvas
        ref="canvas"
        width="640" height="384"
        style="position:absolute; top:0; left:0; width:640px; height:384px; z-index:10; pointer-events:none; background:transparent;"
      ></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import {
    FilesetResolver,
    PoseLandmarker,
    FaceLandmarker,
  } from '@mediapipe/tasks-vision'
  
  const video = ref(null)
  const canvas = ref(null)
  let poseLandmarker, faceLandmarker
  let active = true
  
  function analyzeFaceExpression(faceLandmarks) {
    const LEFT_MOUTH = 61
    const RIGHT_MOUTH = 291
    const TOP_LIP = 13
    const BOTTOM_LIP = 14
    const left = faceLandmarks[LEFT_MOUTH]
    const right = faceLandmarks[RIGHT_MOUTH]
    const top = faceLandmarks[TOP_LIP]
    const bottom = faceLandmarks[BOTTOM_LIP]
    const slope = (left.y - right.y) / ((left.x - right.x) + 1e-6)
    const mouthOpen = Math.abs(top.y - bottom.y)
    const mouthWidth = Math.abs(left.x - right.x)
    if (mouthOpen > 0.07 && mouthWidth > 0.05) {
      return '입벌림'
    } else if (slope < -0.03) {
      return '왼쪽 미소'
    } else if (slope > 0.03) {
      return '오른쪽 미소'
    } else if (mouthOpen < 0.04) {
      return '무표정'
    } else {
      return '미소'
    }
  }
  
  function analyzeLegSpread(poseLandmarks) {
    const LEFT_ANKLE = 27, RIGHT_ANKLE = 28
    const LEFT_KNEE = 25, RIGHT_KNEE = 26
    if (
      !poseLandmarks[LEFT_ANKLE] || !poseLandmarks[RIGHT_ANKLE] ||
      !poseLandmarks[LEFT_KNEE] || !poseLandmarks[RIGHT_KNEE]
    ) return { ankleSpread: 0, kneeSpread: 0 }
    const ankleSpread = Math.abs(poseLandmarks[LEFT_ANKLE].x - poseLandmarks[RIGHT_ANKLE].x)
    const kneeSpread = Math.abs(poseLandmarks[LEFT_KNEE].x - poseLandmarks[RIGHT_KNEE].x)
    return { ankleSpread, kneeSpread }
  }
  
  const SIMPLE_POSE_CONNECTIONS = [
    [11, 13], [13, 15], [12, 14], [14, 16],
    [11, 12], [23, 24],
    [23, 25], [25, 27], [24, 26], [26, 28],
    [27, 31], [28, 32]
  ]
  
  const poseColors = ['red', 'blue']
  const faceColors = ['lime', 'yellow']
  
  onMounted(async () => {
    while (!video.value) {
      await new Promise(r => requestAnimationFrame(r))
    }
  
    // ★ 카메라 해상도 늘리기
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 384 }
    })
    video.value.srcObject = stream
    await new Promise(resolve => {
      video.value.onloadedmetadata = resolve
    })
  
    // 모델 로드 (공식 GCS 경로)
    const vision = await FilesetResolver.forVisionTasks(
      'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm'
    )
  
    poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
      baseOptions: {
        modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task'
      },
      runningMode: 'VIDEO',
      numPoses: 2,
      outputSegmentationMasks: false
    })
  
    faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
      baseOptions: {
        modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task'
      },
      runningMode: 'VIDEO',
      numFaces: 2,
      outputFaceBlendshapes: false,
      outputFacialTransformationMatrixes: false
    })
  
    const analyze = () => {
      if (!active) return
      const ctx = canvas.value.getContext('2d')
      ctx.clearRect(0, 0, 640, 384)
      ctx.drawImage(video.value, 0, 0, 640, 384)
  
      // Pose
      const poses = poseLandmarker.detectForVideo(
        video.value,
        performance.now()
      )
  
      for (let i = 0; i < (poses.landmarks?.length || 0); i++) {
        const color = poseColors[i % 2]
        const landmarks = poses.landmarks[i]
        for (let j = 0; j < landmarks.length; j++) {
          const pt = landmarks[j]
          ctx.beginPath()
          ctx.arc(pt.x * 640, pt.y * 384, 4, 0, 2 * Math.PI)
          ctx.fillStyle = color
          ctx.fill()
        }
        ctx.strokeStyle = color
        ctx.lineWidth = 2
        for (const [start, end] of SIMPLE_POSE_CONNECTIONS) {
          const s = landmarks[start], e = landmarks[end]
          if (s && e) {
            ctx.beginPath()
            ctx.moveTo(s.x * 640, s.y * 384)
            ctx.lineTo(e.x * 640, e.y * 384)
            ctx.stroke()
          }
        }
        // --- 무릎 또는 발목 spread 중 하나라도 임계값 초과시 쩍벌 ---
        const { ankleSpread, kneeSpread } = analyzeLegSpread(landmarks)
        let spreadLabel = ''
        if (ankleSpread > 0.3 || kneeSpread > 0.3) {
          spreadLabel = `다리 벌림: 넓음 (무릎:${kneeSpread.toFixed(2)}, 발목:${ankleSpread.toFixed(2)})`
        } else if (ankleSpread > 0.18 || kneeSpread > 0.18) {
          spreadLabel = `다리 벌림: 약간 (무릎:${kneeSpread.toFixed(2)}, 발목:${ankleSpread.toFixed(2)})`
        } else {
          spreadLabel = `다리 벌림: 정상 (무릎:${kneeSpread.toFixed(2)}, 발목:${ankleSpread.toFixed(2)})`
        }
        const lmk = landmarks[11] // LEFT_SHOULDER
        if (lmk) {
          ctx.font = 'bold 13px sans-serif'
          ctx.fillStyle = color
          ctx.fillText(`Person${i+1}: ${spreadLabel}`, lmk.x * 640, lmk.y * 384 - 10)
        }
      }
  
      // FaceMesh
      const faces = faceLandmarker.detectForVideo(
        video.value,
        performance.now()
      )
  
      for (let i = 0; i < (faces.faceLandmarks?.length || 0); i++) {
        const color = faceColors[i % 2]
        const faceLandmarks = faces.faceLandmarks[i]
        for (let j = 0; j < faceLandmarks.length; j++) {
          const pt = faceLandmarks[j]
          ctx.beginPath()
          ctx.arc(pt.x * 640, pt.y * 384, 1.8, 0, 2 * Math.PI)
          ctx.fillStyle = color
          ctx.fill()
        }
        const exp = analyzeFaceExpression(faceLandmarks)
        const nose = faceLandmarks[1]
        if (nose) {
          ctx.font = 'bold 13px sans-serif'
          ctx.fillStyle = color
          ctx.fillText(`표정: ${exp}`, nose.x * 640, nose.y * 384 - 10)
        }
      }
      requestAnimationFrame(analyze)
    }
    analyze()
  })
  
  onBeforeUnmount(() => {
    active = false
  })
  </script>
  