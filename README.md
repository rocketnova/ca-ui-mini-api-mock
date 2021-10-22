# README

An extremely tiny mock API gateway for testing against https://github.com/cagov/ui-claim-tracker.

Primary use case is to test against strange and unlikely edge cases.

## Usage

Use in conjunction with modHeader. This mock API recognizes the following `uniqueNumber` values:

- `happy_path`: Returns a correctly formed API gateway response
- `missing_unique_number`: Returns a null response with no unique number
- `mismatched_unique_number`: Returns a non-matching unique number and a null response
- `unknown_program`: Returns an unknown Program Type
- `not_mismatched_is_null`: Returns a null response with a matching unique number
- `date_too_early`: Returns a `requestDate` that is outside the expected range
- `invalid_time_slot`: Returns a `timeDesc` that is outside the expected range

Sending no `uniqueNumber` request header or `uniqueNumber` with an empty string both result in the `missing_unique_number` response.

All other values return an "API Gateway response is not 200" error.
