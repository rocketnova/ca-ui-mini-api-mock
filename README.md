# README

An extremely tiny mock API gateway for testing against https://github.com/cagov/ui-claim-tracker.

Primary use case is to test against strange and unlikely edge cases.

## How to Run

1. Make sure `docker` and `docker-compose` are installed
2. Run `docker-compose up -d --build` to build the image and start the container in the background
3. Connect to the API at `localhost:8888`
4. To stop the container, run `docker-compose down`

## Usage

Use in conjunction with modHeader. This mock API recognizes the following `uniqueNumber` values:

Happy paths values:

- `happy_path`: Returns a correctly formed API gateway response
- `scenario2`: Returns a correctly formed API gateway response for scenario 2

Unhappy path values:

- `missing_unique_number`: Returns a null response with no unique number
- `mismatched_unique_number`: Returns a non-matching unique number and a null response
- `unknown_program`: Returns an unknown Program Type
- `not_mismatched_is_null`: Returns a null response with a matching unique number
- `date_too_early`: Returns a `requestDate` that is outside the expected range
- `invalid_time_slot`: Returns a `timeDesc` that is outside the expected range
- `invalid_feded_bye`: Returns a response for a valid `isBYE` FED-ED, but with empty string for `benefitYearEndDate`

