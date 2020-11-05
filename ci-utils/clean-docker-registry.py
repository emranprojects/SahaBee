#!/usr/bin/env python
import requests
import argparse

args = None


def main():
    handle_args()
    resp = requests.get(url=f"https://gitlab.com/api/v4/projects/{args.project_id}/registry/repositories",
                        headers={'PRIVATE-TOKEN': args.access_token})
    repos = resp.json()
    for repo in repos:
        if repo['name'] == args.repo or repo['path'] == args.repo or repo['location'] == args.repo:
            clean_repo(repo['id'], args.prefix)
            break
    print("Finished!")


def handle_args():
    parser = argparse.ArgumentParser(description='Removes junk tags from gitlab docker registry.')
    parser.add_argument('--project-id',
                        action='store',
                        help='Gitlab project id',
                        required=True)
    parser.add_argument('--access-token',
                        action='store',
                        help='Gitlab access token for API calls',
                        required=True)
    parser.add_argument('--repo',
                        action='store',
                        help='Docker image name. e.g. awesome-image or username/projectname/awesome-image',
                        required=True)
    parser.add_argument('--prefix',
                        action='store',
                        help='Junk tags prefix. e.g. --prefix "snapshot-" implies removing images like awsome-image:snapshot-1',
                        required=True)
    global args
    args = parser.parse_args()


def clean_repo(repo_id, tag_prefix):
    r = 1
    while True:
        resp = requests.get(
            url=f"https://gitlab.com/api/v4/projects/{args.project_id}/registry/repositories/{repo_id}/tags/",
            headers={'PRIVATE-TOKEN': args.access_token})
        tags = resp.json()
        junk_tags = [t for t in tags if t['name'].startswith(tag_prefix)]
        if len(junk_tags) == 0:
            print("No more junk tags.")
            break
        print(f'Round {r}. Found {len(junk_tags)} junk tags. Going to delete...')
        for num, tag in enumerate(junk_tags, start=1):
            resp = requests.delete(url=f"https://gitlab.com/api/v4/projects/{args.project_id}"
                                       f"/registry/repositories/{repo_id}/tags/{tag['name']}",
                                   headers={'PRIVATE-TOKEN': args.access_token})
            resp.raise_for_status()
            print(f"Deleted {num}/{len(junk_tags)}: {tag['path']}")
        r += 1


main()
