from store import store_current_state_in_bq

def main(request):
    # Store current state in BigQuery
    store_current_state_in_bq()

    return 'Done'