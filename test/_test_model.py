from datetime import datetime

from sqlalchemy.exc import IntegrityError

from test import ModelTestCase
from planner.model import (
    Client, EngagementStatus, EngagementAlignment, Contact, Iteration,
    Engagement, ActualEngagementIteration,
    EngagementComplexity, EngagementProbability, EngagementSustainability
)


class TestClient(ModelTestCase):
    def test_client_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(Client)

    def test_client_should_have_correct_contact(self):
        expected = Contact(forename="Mc", surname="Test")
        with self.transaction() as db:
            db.add(Client(name="Name", contactid=1))
            db.add(expected)

        with self.transaction() as db:
            actual = db.query(Client).first().contact

        self.assertEquals(expected, actual)


class TestEngagementStatus(ModelTestCase):
    def test_engagement_status_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(EngagementStatus)


class TestEngagementAlignment(ModelTestCase):
    def test_engagement_alignment_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(EngagementAlignment, value=1)

    def test_engagement_alignment_should_always_have_a_valid_value(self):
        self.assertHasValidValue(EngagementAlignment, 0.0, 1.0, name="Name")

    def test_engagement_alignment_should_always_have_a_unique_value(self):
        self.assertHasUniqueValue(EngagementAlignment, name="Name")


class TestEngagementSustainability(ModelTestCase):
    def test_engagement_sustainability_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(EngagementSustainability, value=1)

    def test_engagement_sustainability_should_always_have_a_valid_value(self):
        self.assertHasValidValue(EngagementSustainability, 0.0, 1.0,
                                 name="Name")

    def test_engagement_sustainability_should_always_have_a_unique_value(self):
        self.assertHasUniqueValue(EngagementSustainability, name="Name")


class TestEngagementProbability(ModelTestCase):
    def test_engagement_probability_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(EngagementProbability, value=0.5)

    def test_engagement_probability_should_always_have_a_unique_value(self):
        self.assertHasUniqueValue(EngagementProbability, name="Name")

    def test_engagement_probability_should_always_have_a_valid_value(self):
        self.assertHasValidValue(EngagementProbability, 0.0, 1.0, name="Name")


class TestEngagementComplexity(ModelTestCase):
    def test_engagement_complexity_should_always_have_a_unique_name(self):
        self.assertHasUniqueName(EngagementComplexity, value=0.5)

    def test_engagement_complexity_should_always_have_a_unique_value(self):
        self.assertHasUniqueValue(EngagementComplexity, name="Name")

    def test_engagement_complexity_should_always_have_a_valid_value(self):
        self.assertHasValidValue(EngagementComplexity, 0.1, 2.0, name="Name")


class TestIteration(ModelTestCase):
    def test_iteration_should_have_a_start_date(self):
        with self.assertRaises(IntegrityError):
            with self.transaction() as db:
                db.add(Iteration(startdate=None))

    def test_iteration_should_accurately_represent_actual_engagements(self):
        expected = Engagement(name="Name", revenue=0)
        with self.transaction() as db:
            db.add(Iteration(startdate=datetime.today()))
            db.add(expected)
            db.execute(ActualEngagementIteration.insert(values=(1, 1)))

        with self.transaction() as db:
            actual = db.query(Iteration).first().actual

        self.assertEquals(expected, actual[0])
        self.assertTrue(len(actual) == 1)
