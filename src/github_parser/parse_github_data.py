import os
import psycopg2
import requests
from datetime import datetime
from typing import List

HOST = "http://51.250.2.103:8080"


def fetch_top_repositories(sorting_method: str) -> List[dict]:
    url = f"{HOST}/api/repos/top100?sorting_method={sorting_method}"
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"An error occurred while fetching top repositories: {e}")
        return []
    data = response.json()
    return data


def fetch_repo_activity(repo: str, since: str, until: str) -> List[dict]:
    url = f"{HOST}/api/repos/{repo}/activity?since={since}&until={until}"
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"An error occurred while fetching repo activity: {e}")
        return []
    data = response.json()
    return data


def save_repositories_to_db(repos: List[dict], conn) -> List[int]:
    repo_ids = []
    cursor = None
    try:
        cursor = conn.cursor()
        for repo in repos:
            cursor.execute("""
                INSERT INTO Repositories (
                    repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (repo) DO UPDATE
                SET position_cur = EXCLUDED.position_cur, position_prev = EXCLUDED.position_prev, 
                stars = EXCLUDED.stars, watchers = EXCLUDED.watchers, forks = EXCLUDED.forks, 
                open_issues = EXCLUDED.open_issues, language = EXCLUDED.language
                RETURNING id;
            """, (repo['repo'], repo['owner'], repo['position_cur'], repo['position_prev'],
                  repo['stars'], repo['watchers'], repo['forks'], repo['open_issues'], repo['language']))
            repo_id = cursor.fetchone()[0]
            repo_ids.append(repo_id)
        conn.commit()
    except Exception as e:
        print(f"An error occurred while saving repositories to DB: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
    return repo_ids


def save_repo_activity_to_db(repo_id: int, activity: List[dict], conn) -> None:
    cursor = None
    try:
        cursor = conn.cursor()
        for activity_item in activity:
            date = datetime.strptime(activity_item['date'], "%Y-%m-%dT%H:%M:%S").date()
            cursor.execute("""
                INSERT INTO RepoActivity (repo_id, date, commits, authors)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (repo_id, date) DO UPDATE
                SET commits = EXCLUDED.commits, authors = EXCLUDED.authors;
            """, (repo_id, date, activity_item['commits'], activity_item['authors']))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while saving repo activity to DB: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def initialize_sql_tables(conn):
    cursor = conn.cursor()
    with open("init.sql", 'r') as initialize_sql_if_not_exists:
        cursor.execute(initialize_sql_if_not_exists.read())
    cursor.close()


def get_last_repo_record(repos_id, conn):
    cursor = conn.cursor()
    cursor.execute("""
                        SELECT date
                        FROM RepoActivity
                        WHERE repo_id = %s
                        ORDER BY date DESC
                        LIMIT 1;
                    """, (repos_id,)
                   )
    last_record = cursor.fetchone()
    cursor.close()
    return last_record


def parse_github_data(event, context):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ['POSTGRES_HOST']
        )

        initialize_sql_tables(conn)

        top_repos = fetch_top_repositories("stars")
        repos_ids = save_repositories_to_db(top_repos, conn)

        for idx, repo in enumerate(top_repos):
            last_record = get_last_repo_record(repos_ids[idx], conn)
            if last_record is None:
                since = "1970-01-01"
            else:
                since = last_record[0].strftime("%Y-%m-%d")
            until = datetime.now().strftime("%Y-%m-%d")

            activity = fetch_repo_activity(repo['repo'], since, until)
            save_repo_activity_to_db(repos_ids[idx], activity, conn)

    except Exception as e:
        print(f"An error occurred while parsing GitHub data: {e}")
    finally:
        if conn:
            conn.close()
