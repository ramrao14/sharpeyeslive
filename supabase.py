import requests

SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dGN3dHpvbmRoZ3p3dXlnd21qIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTI5OTgwMTgsImV4cCI6MjAwODU3NDAxOH0.MrF7ig3Hy7EA9DpUn7UacKYZS4CpIBnD1MiiuTWmIP0'
PROFILES_ENDPOINT = 'https://zutcwtzondhgzwuygwmj.supabase.co/rest/v1/profiles'
VIDEOS_ENDPOINT = 'https://zutcwtzondhgzwuygwmj.supabase.co/rest/v1/videos'
QUESTIONS_ENDPOINT = 'https://zutcwtzondhgzwuygwmj.supabase.co/rest/v1/questions'
QUESTIONS_ANSWERED_ENDPOINT = 'https://zutcwtzondhgzwuygwmj.supabase.co/rest/v1/questions_answered'
REFERRALS_ENDPOINT = 'https://zutcwtzondhgzwuygwmj.supabase.co/rest/v1/referrals'
TICKETS_ENDPOINT = 'https://zutcwtzondhgzwuygwmj.supabase.co/rest/v1/tickets'

QUESTION_SCORE = 10


def get_active_videos():
    params = {'apikey': SUPABASE_ANON_KEY,
              'select': 'id,brand_name,provider,provider_id,embed_url,thumbnail_url,brand_logo_url,created_at,campaign_name,active_sequence',
              'is_active': 'eq.True'}
    videos = requests.get(VIDEOS_ENDPOINT, params=params).json()
    return videos


def get_questions(video_id, active_sequence):
    params = {'apikey': SUPABASE_ANON_KEY,
              'video_id': f'eq.{video_id}',
              'sequence': f'eq.{active_sequence}'}
    questions = requests.get(QUESTIONS_ENDPOINT, params=params).json()
    return questions


def process_answer(user_id, question_id, video_id):
    params = {'apikey': SUPABASE_ANON_KEY}
    payload = {'user_id': user_id,
               'question_id': question_id,
               'video_id': video_id}
    return requests.post(QUESTIONS_ANSWERED_ENDPOINT, params=params, data=payload)


def process_referrer(referrer, signup_user):
    params = {'apikey': SUPABASE_ANON_KEY}
    payload = {'referrer': referrer,
               'signup_user': signup_user}
    return requests.post(REFERRALS_ENDPOINT, params=params, data=payload)


def get_quiz_score(user_id, video_id):
    params = {'apikey': SUPABASE_ANON_KEY,
              'user_id': f'eq.{user_id}',
              'video_id': f'eq.{video_id}'}
    questions = requests.get(QUESTIONS_ANSWERED_ENDPOINT, params=params).json()
    return len(questions)*QUESTION_SCORE


def get_total_score(user_id):
    params = {'apikey': SUPABASE_ANON_KEY,
              'user_id': f'eq.{user_id}'}
    questions = requests.get(QUESTIONS_ANSWERED_ENDPOINT, params=params).json()
    return len(questions)*QUESTION_SCORE

def get_user_score(user_id):
    params = {'apikey': SUPABASE_ANON_KEY,
              'select': 'score',
              'user_id': f'eq.{user_id}'}
    score = requests.get(PROFILES_ENDPOINT, params=params).json()[0]['score']
    return score

def get_user_tickets(user_id):
    params = {'apikey': SUPABASE_ANON_KEY,
              'user_id': f'eq.{user_id}'}
    tickets = requests.get(TICKETS_ENDPOINT, params=params).json()
    return tickets

def purchase_ticket(user_id, ticket):
    params = {'apikey': SUPABASE_ANON_KEY}
    payload = {'user_id': user_id,
               'num_1': ticket['num_1'],
               'num_2': ticket['num_2'],
               'num_3': ticket['num_3'],
               'num_4': ticket['num_4'],
               'num_5': ticket['num_5'],
               'num_powerball': ticket['num_powerball'],
               }
    return requests.post(TICKETS_ENDPOINT, params=params, data=payload)