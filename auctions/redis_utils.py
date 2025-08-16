# auctions/redis_utils.py
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
HIGHEST_BID_KEY_PREFIX = 'auction_highest_bid:'

def get_highest_bid(auction_id):
    key = f'{HIGHEST_BID_KEY_PREFIX}{auction_id}'
    bid = redis_client.get(key)
    if bid is None:
        return None
    return float(bid.decode('utf-8'))

def set_highest_bid(auction_id, amount):
    key = f'{HIGHEST_BID_KEY_PREFIX}{auction_id}'
    redis_client.set(key, amount)