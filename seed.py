from datetime import timedelta
from django.utils import timezone
from task.models.users import User
from task.models.test import Test
from task.models.course import Course
from task.models.payment import Payment
from task.models.test import TestRegistration
from task.models.course import CourseRegistration

print("Seeding 데이터 생성")

"""
1. 사용자
"""
if not User.objects.exists():
    users = [
        User(email="test1@example.com"),
        User(email="test2@example.com"),
        User(email="test3@example.com"),
    ]
    for u in users:
        u.set_password("1234")
        u.save()
    print("Users created.")
else:
    print("Users already exist, skipping.")

"""
2. 시험 목록 생성 (3가지 상태 x 3개 = 총 9개 가능)
"""
now = timezone.now()

if not Test.objects.exists():
    test_cases = [
        # 진행 중 (available)
        ("진행 중 시험 1", now - timedelta(days=1), now + timedelta(days=3)),
        ("진행 중 시험 2", now - timedelta(hours=6), now + timedelta(days=1)),
        ("진행 중 시험 3", now - timedelta(days=2), now + timedelta(days=2)),
        # 시작 전 (upcoming)
        ("시작 전 시험 1", now + timedelta(days=1), now + timedelta(days=4)),
        ("시작 전 시험 2", now + timedelta(days=3), now + timedelta(days=10)),
        ("시작 전 시험 3", now + timedelta(hours=12), now + timedelta(days=2)),
        # 종료됨 (closed)
        ("종료된 시험 1", now - timedelta(days=10), now - timedelta(days=3)),
        ("종료된 시험 2", now - timedelta(days=5), now - timedelta(days=1)),
        ("종료된 시험 3", now - timedelta(days=15), now - timedelta(days=8)),
    ]

    for title, start, end in test_cases:
        Test.objects.create(title=title, start_at=start, end_at=end)

    print("Test 데이터 9건 생성 완료 (진행/대기/종료 포함).")
else:
    print("Test already exist, skipping.")

"""
3. 수업 목록 생성 (3가지 상태 x 3개 = 총 9개 가능)
"""
if not Course.objects.exists():
    course_cases = [
        # 진행 중 (available)
        ("진행 중 수업 1", now - timedelta(days=2), now + timedelta(days=4)),
        ("진행 중 수업 2", now - timedelta(hours=12), now + timedelta(days=2)),
        ("진행 중 수업 3", now - timedelta(days=1), now + timedelta(days=1)),
        # 시작 전 (upcoming)
        ("시작 전 수업 1", now + timedelta(days=1), now + timedelta(days=5)),
        ("시작 전 수업 2", now + timedelta(days=3), now + timedelta(days=7)),
        ("시작 전 수업 3", now + timedelta(hours=6), now + timedelta(days=2)),
        # 종료됨 (closed)
        ("종료된 수업 1", now - timedelta(days=10), now - timedelta(days=5)),
        ("종료된 수업 2", now - timedelta(days=7), now - timedelta(days=2)),
        ("종료된 수업 3", now - timedelta(days=15), now - timedelta(days=8)),
    ]

    for title, start, end in course_cases:
        Course.objects.create(title=title, start_at=start, end_at=end)

    print("Course 데이터 9건 생성 완료 (진행/대기/종료 포함).")
else:
    print("Course already exist, skipping.")

"""
3. 시험 등록 및 결제 정보 생성
"""
user = User.objects.first()
test = Test.objects.filter(title__startswith="진행 중").first()
if not TestRegistration.objects.filter(user=user, test=test).exists():
    payment = Payment.objects.create(
        user=user,
        amount=45000,
        payment_method="kakaopay",
        test=test,
        status="paid",
    )
    TestRegistration.objects.create(user=user, test=test, status="applied")
    print("TestRegistration + Payment created.")
else:
    print("TestRegistration already exists, skipping.")


"""
4. 수업 등록 및 결제 정보 생성
"""
course = Course.objects.filter(title__startswith="진행 중").first()
if not CourseRegistration.objects.filter(user=user, course=course).exists():
    payment = Payment.objects.create(
        user=user,
        amount=35000,
        payment_method="card",
        course=course,
        status="paid",
    )
    CourseRegistration.objects.create(
        user=user, course=course, status="enrolled"
    )
    print("CourseRegistration + Payment created.")
else:
    print("CourseRegistration already exists, skipping.")

print("Seeding completed successfully!")
