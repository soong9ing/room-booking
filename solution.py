# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9
CLOSE_HOUR = 21
MAX_HOURS = 3
MAX_PER_PERSON_PER_DAY = 2


def _is_int(x):
    """정수인지 확인 (True/False는 정수로 보지 않음)"""
    return type(x) is int


def _valid_place(room, day):
    """있는 강의실·요일인지 확인 (문자열만 인정)"""
    return (
        isinstance(room, str) and isinstance(day, str)
        and room in ROOMS and day in DAYS
    )


class RoomBooking:
    def __init__(self):
        # 예약 목록: 각 예약은 {"room", "day", "start", "end", "name"}
        self._bookings = []

    def book(self, room, day, start, end, name):
        # 1. 없는 강의실·요일
        if not _valid_place(room, day):
            return False
        # 2. 정수가 아닌 시간 (bool 제외)
        if not (_is_int(start) and _is_int(end)):
            return False
        # 3. 운영 시간 밖
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return False
        # 4. 시작 >= 끝
        if start >= end:
            return False
        # 5. 3시간 초과
        if end - start > MAX_HOURS:
            return False
        # 6. 같은 강의실·요일 시간 겹침 (끝나는 시각에 바로 시작은 허용)
        for b in self._bookings:
            if b["room"] == room and b["day"] == day:
                if start < b["end"] and b["start"] < end:
                    return False
        # 7. 같은 사람은 같은 요일 최대 2건 (강의실 합산)
        count = sum(1 for b in self._bookings if b["day"] == day and b["name"] == name)
        if count >= MAX_PER_PERSON_PER_DAY:
            return False

        self._bookings.append(
            {"room": room, "day": day, "start": start, "end": end, "name": name}
        )
        return True

    def cancel(self, room, day, start, name):
        if not _valid_place(room, day) or not _is_int(start):
            return False
        for i, b in enumerate(self._bookings):
            if b["room"] == room and b["day"] == day and b["start"] == start:
                if b["name"] != name:
                    return False
                del self._bookings[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not _valid_place(room, day):
            return []
        result = [
            (b["start"], b["end"], b["name"])
            for b in self._bookings
            if b["room"] == room and b["day"] == day
        ]
        result.sort(key=lambda t: t[0])
        return result
