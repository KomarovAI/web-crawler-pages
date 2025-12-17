#!/bin/bash
# Run deployment workflow with default parameters
# curl -X POST \$ https://api.github.com/repos/KomarovAI/web-crawler-pages/actions/workflows/deploy.yml/dispatches \$ -H "Authorization: Bearer YOUR_TOKEN" \$ -H "Accept: application/vnd.github.v3+json" \$ -d '{"ref":"main","inputs":{"artifact_name":"archive-a370f4484bdb1bff56f115d24914942a47de60c601b762df5cbb4170301695a2","run_id":"20290432867"}}'

echo "To deploy: Go to https://github.com/KomarovAI/web-crawler-pages/actions/workflows/deploy.yml"
echo "Parameters:"
echo "  artifact_name: archive-a370f4484bdb1bff56f115d24914942a47de60c601b762df5cbb4170301695a2"
echo "  run_id: 20290432867"
