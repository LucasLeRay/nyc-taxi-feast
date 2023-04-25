from src.utils import StrEnum


class SourceTrips(StrEnum):
    """Columns defined in trips source table"""
    VENDOR_ID = "vendor_id"
    PICKUP_DATETIME = "pickup_datetime"
    DROPOFF_DATETIME = "dropoff_datetime"
    PASSENGER_COUNT = "passenger_count"
    TRIP_DISTANCE = "trip_distance"
    PICKUP_LONGITUDE = "pickup_longitude"
    PICKUP_LATITUDE = "pickup_latitude"
    RATE_CODE = "rate_code"
    STORE_AND_FWD_FLAG = "store_and_fwd_flag"
    DROPOFF_LONGITUDE = "dropoff_longitude"
    DROPOFF_LATITUDE = "dropoff_latitude"
    PAYMENT_TYPE = "payment_type"
    FARE_AMOUNT = "fare_amount"
    EXTRA = "extra"
    MTA_TAX = "mta_tax"
    TIP_AMOUNT = "tip_amount"
    TOLLS_AMOUNT = "tolls_amount"
    IMP_SURCHARGE = "imp_surcharge"
    TOTAL_AMOUNT = "total_amount"
