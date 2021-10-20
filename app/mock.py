from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

import falcon

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ClaimResource:
    def on_get(self, req, resp):
        """Handles GET requests"""

        # Parse the query string.
        queries = parse_qs(req.query_string)
        for num in queries['uniqueNumber']:
            result = self.lookup_unique_number(num)
            if result != None:
                resp.media = result
                resp.status = falcon.HTTP_200  # This is the default status
                break

        if not resp.media:
            resp.status = falcon.HTTP_404

    def lookup_unique_number(self, unique_number):
        match unique_number:
            case "happy_path":
                return {
                    "uniqueNumber": "happy_path",
                    "claimDetails": {
                        "programType": "UI",
                        "benefitYearStartDate": "2013-07-21T00:00:00",
                        "benefitYearEndDate": "2014-07-19T00:00:00",
                        "claimBalance": 5632.00,
                        "weeklyBenefitAmount": 256.00,
                        "lastPaymentIssued": "2016-08-26T00:00:00",
                        "lastPaymentAmount": 336.00,
                        "monetaryStatus": "Active"
                    },
                    "hasCertificationWeeksAvailable": False,
                    "hasPendingWeeks": False,
                    "pendingDetermination": [
                        {
                            "scheduleDate": "2021-09-22T00:00:00",
                            "timeSlotDesc": "8-10",
                            "requestDate": "2021-09-16T00:00:00",
                            "determinationStatus": None,
                            "willCallIndicator": False,
                            "spokenLanguageCode": "E",
                            "spokenLanguageDesc": "English"
                        }
                    ]
                }

            case "missing_unique_number":
                return {
                  "uniqueNumber": None,
                  "claimDetails": None,
                  "hasCertificationWeeksAvailable": False,
                  "hasPendingWeeks": False,
                  "pendingDetermination": None
                }

            case "mismatched_unique_number":
                return {
                  "uniqueNumber": "some_other_number",
                  "claimDetails": {
                    "programType": "",
                    "benefitYearStartDate": None,
                    "benefitYearEndDate": None,
                    "claimBalance": None,
                    "weeklyBenefitAmount": None,
                    "lastPaymentIssued": None,
                    "lastPaymentAmount": None,
                    "monetaryStatus": ""
                  },
                  "hasCertificationWeeksAvailable": False,
                  "hasPendingWeeks": False,
                  "pendingDetermination": []
                }

            case "not_mismatched_is_null":
                return {
                  "uniqueNumber": "not_mismatched_is_null",
                  "claimDetails": {
                    "programType": "",
                    "benefitYearStartDate": None,
                    "benefitYearEndDate": None,
                    "claimBalance": None,
                    "weeklyBenefitAmount": None,
                    "lastPaymentIssued": None,
                    "lastPaymentAmount": None,
                    "monetaryStatus": ""
                  },
                  "hasCertificationWeeksAvailable": False,
                  "hasPendingWeeks": False,
                  "pendingDetermination": []
                }

            case "unknown_program":
                return {
                    "uniqueNumber": "unknown_program",
                    "claimDetails": {
                        "programType": "Unknown Other Program!",
                        "benefitYearStartDate": "2013-07-21T00:00:00",
                        "benefitYearEndDate": "2014-07-19T00:00:00",
                        "claimBalance": 5632.00,
                        "weeklyBenefitAmount": 256.00,
                        "lastPaymentIssued": "2016-08-26T00:00:00",
                        "lastPaymentAmount": 336.00,
                        "monetaryStatus": "Active"
                    },
                    "hasCertificationWeeksAvailable": False,
                    "hasPendingWeeks": False,
                    "pendingDetermination": []
                }

            case "date_too_early":
                return {
                    "uniqueNumber": "date_too_early",
                    "claimDetails": {
                        "programType": "UI",
                        "benefitYearStartDate": "2013-07-21T00:00:00",
                        "benefitYearEndDate": "2014-07-19T00:00:00",
                        "claimBalance": 5632.00,
                        "weeklyBenefitAmount": 256.00,
                        "lastPaymentIssued": "2016-08-26T00:00:00",
                        "lastPaymentAmount": 336.00,
                        "monetaryStatus": "Active"
                    },
                    "hasCertificationWeeksAvailable": False,
                    "hasPendingWeeks": False,
                    "pendingDetermination": [
                        {
                            "scheduleDate": "",
                            "timeSlotDesc": "8-10",
                            "requestDate": "1969-09-16T00:00:00",
                            "determinationStatus": None,
                            "willCallIndicator": False,
                            "spokenLanguageCode": "E",
                            "spokenLanguageDesc": "English"
                        }
                    ]
                }

            case "invalid_time_slot":
                return {
                    "uniqueNumber": "invalid_time_slot",
                    "claimDetails": {
                        "programType": "UI",
                        "benefitYearStartDate": "2013-07-21T00:00:00",
                        "benefitYearEndDate": "2014-07-19T00:00:00",
                        "claimBalance": 5632.00,
                        "weeklyBenefitAmount": 256.00,
                        "lastPaymentIssued": "2016-08-26T00:00:00",
                        "lastPaymentAmount": 336.00,
                        "monetaryStatus": "Active"
                    },
                    "hasCertificationWeeksAvailable": False,
                    "hasPendingWeeks": False,
                    "pendingDetermination": [
                        {
                            "scheduleDate": "2021-12-01T00:00:00",
                            "timeSlotDesc": "13-19",
                            "requestDate": "2020-09-16T00:00:00",
                            "determinationStatus": None,
                            "willCallIndicator": False,
                            "spokenLanguageCode": "E",
                            "spokenLanguageDesc": "English"
                        }
                    ]
                }


            case _:
                return None

# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
claim = ClaimResource()

# claim will handle all requests to the '/GetClaimStatus' URL path
app.add_route('/GetClaimStatus', claim)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
