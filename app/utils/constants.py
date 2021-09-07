from datetime import time

RESTAURANT_OPEN_TIME=time(13, 0)
RESTAURANT_CLOSE_TIME=time(23, 0)
MAX_AVAILABLE_DAYS=3
SLOT_DURATION_IN_MINUTES=15

TABLE_CAPACITY_ERROR="Please make sure you choose a table with capacity more than or equal your required number." 
RESERVATION_DATE_IN_THE_PAST="Date can't be in the past or far from 3 days."
RESERVATION_FOR_MORE_THAN_12_OR_LESS_THAN_1="Table capacity should be between 1: 12"
RESERVATION_CHECK='Available slot for the tables that fits the required number of people sorted by bestFit first.'