interface Interviewee {
  name: string;
  id: number;
}

interface InterviewSchedule {
  interviewDate: number[]; // [YYYY, MM, DD]
  timeRange: string;       // '09:00 - 10:00'
  roomName: string;
  interviewers: string[];
  interviewees: Interviewee[];
  interviewId: number;
}

interface ScheduleResponse {
  schedules: InterviewSchedule[];
  message: string;
}

interface ApiResponse {
  data: Array<{
    interviewId: number;
    intervieweeId: number;
    name: string;
    startAt: string; // ISO 8601 문자열
    endAt: string;   // ISO 8601 문자열
    status: string;
    score: number | null;
    interviewers: string;
    roomNo: string;
    comment: string | null;
    createdAt: string; // ISO 8601 문자열
  }>;
  totalCount: number;
}

export const getInterviewSchedules = async (date: string): Promise<ScheduleResponse> => {
  try {
    const response = await fetch(`http://3.38.218.18:8080/api/v1/interviews/simple`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Content-Type이 JSON이 아닐 경우 예외 처리
    const contentType = response.headers.get('content-type');
    if (!response.ok || !contentType || !contentType.includes('application/json')) {
      return {
        schedules: [],
        message: '면접 일정 없음'
      };
    }

    // JSON 파싱 시도, 실패하면 빈 배열 반환
    let apiResponse: ApiResponse;
    try {
      apiResponse = await response.json();
    } catch (e) {
      return {
        schedules: [],
        message: '면접 일정 없음'
      };
    }

    const selectedDate = date.split('-').map(Number); // ['2025','06','23'] -> [2025, 6, 23]
    const scheduleMap = new Map<string, InterviewSchedule>();

    apiResponse.data.forEach(item => {
      // startAt, endAt 파싱
      const startDate = new Date(item.startAt);
      const year = startDate.getFullYear();
      const month = startDate.getMonth() + 1;
      const day = startDate.getDate();
      const hour = startDate.getHours();
      const minute = startDate.getMinutes();

      // 날짜가 선택한 날짜와 다르면 스킵
      if (year !== selectedDate[0] || month !== selectedDate[1] || day !== selectedDate[2]) return;

      // 시간대 계산
      const startHour = hour.toString().padStart(2, '0');
      const startMinute = minute.toString().padStart(2, '0');
      // endAt도 필요하면 아래처럼 사용 가능
      // const endDate = new Date(item.endAt);
      // const endHour = endDate.getHours().toString().padStart(2, '0');
      // const endMinute = endDate.getMinutes().toString().padStart(2, '0');
      // const timeRange = `${startHour}:${startMinute} - ${endHour}:${endMinute}`;
      const endHour = (hour + 1).toString().padStart(2, '0'); // 기본적으로 1시간 단위로 가정
      const timeRange = `${startHour}:${startMinute} - ${endHour}:${startMinute}`;

      const key = `${year}-${month}-${day}_${item.roomNo}_${timeRange}`;

      if (!scheduleMap.has(key)) {
        scheduleMap.set(key, {
          interviewDate: [year, month, day],
          timeRange,
          roomName: item.roomNo,
          interviewers: item.interviewers.split(',').map(i => i.trim()),
          interviewees: [],
          interviewId: item.interviewId
        });
      }

      const schedule = scheduleMap.get(key)!;
      schedule.interviewees.push({
        name: item.name,
        id: item.intervieweeId
      });
    });

    return {
      schedules: Array.from(scheduleMap.values()),
      message: '면접 일정 조회 성공'
    };

  } catch (error) {
    console.error('면접 일정 조회 중 오류 발생:', error);
    return {
      schedules: [],
      message: '면접 일정 없음'
    };
  }
};

// 특정 intervieweeId로 simple API에서 면접자 정보를 반환하는 함수
export const getIntervieweeInfoById = async (intervieweeId: number) => {
  try {
    const response = await fetch('http://3.38.218.18:8080/api/v1/interviews/simple', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const contentType = response.headers.get('content-type');
    if (!response.ok || !contentType || !contentType.includes('application/json')) {
      return null;
    }
    const apiResponse = await response.json();
    if (!apiResponse.data || !Array.isArray(apiResponse.data)) return null;
    return apiResponse.data.find((item: any) => item.intervieweeId === intervieweeId) || null;
  } catch (e) {
    console.error('getIntervieweeInfoById 오류:', e);
    return null;
  }
};
