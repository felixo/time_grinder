from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.utils import timezone

from grinder.models import Action, Area, Project


@pytest.fixture
def user():
    return get_user_model().objects.create_user(username="owner")


@pytest.mark.django_db
def test_area_belongs_to_user(user):
    area = Area.objects.create(user=user, name="Health")

    assert area.user == user
    assert area in user.areas.all()


@pytest.mark.django_db
def test_project_can_belong_to_area(user):
    area = Area.objects.create(user=user, name="Health")
    project = Project.objects.create(user=user, area=area, name="Sport")

    assert project.user == user
    assert project.area == area
    assert project in area.projects.all()


@pytest.mark.django_db
def test_project_can_exist_without_area(user):
    project = Project.objects.create(user=user, name="Unsorted")

    assert project.area is None


@pytest.mark.django_db
def test_deleting_area_does_not_delete_project(user):
    area = Area.objects.create(user=user, name="Health")
    project = Project.objects.create(user=user, area=area, name="Sport")

    area.delete()

    project.refresh_from_db()
    assert project.area is None


@pytest.mark.django_db
def test_action_can_belong_to_project(user):
    project = Project.objects.create(user=user, name="Sport")
    action = Action.objects.create(user=user, project=project, duration_seconds=1800)

    assert action.user == user
    assert action.project == project
    assert action in project.actions.all()
    assert not action.is_running


@pytest.mark.django_db
def test_action_can_exist_without_project(user):
    action = Action.objects.create(user=user, duration_seconds=1800)

    assert action.project is None


@pytest.mark.django_db
def test_running_and_stopped_action_states(user):
    started_at = timezone.now() - timedelta(minutes=30)
    running = Action.objects.create(user=user, started_at=started_at)

    assert running.is_running

    running.ended_at = timezone.now()
    running.duration_seconds = 1800
    running.save()

    assert not running.is_running


@pytest.mark.django_db
def test_database_rejects_second_running_action_for_same_user(user):
    Action.objects.create(user=user, started_at=timezone.now())

    with pytest.raises(IntegrityError), transaction.atomic():
        Action.objects.create(user=user, started_at=timezone.now())


@pytest.mark.django_db
def test_database_allows_different_users_to_run_actions():
    user_model = get_user_model()
    first_user = user_model.objects.create_user(username="first")
    second_user = user_model.objects.create_user(username="second")

    first_action = Action.objects.create(user=first_user, started_at=timezone.now())
    second_action = Action.objects.create(user=second_user, started_at=timezone.now())

    assert first_action.is_running
    assert second_action.is_running


@pytest.mark.django_db
def test_database_rejects_invalid_action_time_state(user):
    with pytest.raises(IntegrityError), transaction.atomic():
        Action.objects.create(user=user)
