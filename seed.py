# seed/run.py
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
2. 시험, 수업 목록 생성
"""
now = timezone.now()
if not Test.objects.exists():
    for i in range(3):
        Test.objects.create(
            title=f"Sample Test {i+1}",
            start_at=now,
            end_at=now + timedelta(days=10),
        )
    print("Tests created.")
else:
    print("Tests already exist, skipping.")

if not Course.objects.exists():
    for i in range(3):
        Course.objects.create(
            title=f"Sample Course {i+1}",
            start_at=now,
            end_at=now + timedelta(days=15),
        )
    print("Courses created.")
else:
    print("Courses already exist, skipping.")

"""
3. 시험 등록 및 결제 정보 생성
"""
user = User.objects.first()
test = Test.objects.first()

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
course = Course.objects.first()
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
