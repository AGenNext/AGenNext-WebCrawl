# GitHub Actions Secrets Setup

## Docker Hub Login (Org-Level)

To use org-level secrets for Docker Hub authentication:

### 1. Set Organization Variables

Go to: https://github.com/organizations/AGenNext/settings/variables

Add new variable:
- **Name:** `DOCKERHUB_USERNAME`
- **Value:** your Docker Hub username

### 2. Set Organization Secrets

Go to: https://github.com/organizations/AGenNext/settings/secrets/actions

Add new secret:
- **Name:** `DOCKERHUB_TOKEN`
- **Value:** your Docker Hub access token

> Get token from: https://hub.docker.com/settings/security

### 3. Update Workflow

In `.github/workflows/cd.yml`:

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ vars.DOCKERHUB_USERNAME }}   # org variable
    password: ${{ secrets.DOCKERHUB_TOKEN }}  # org secret
```

### Workflow Access

| Type | Syntax | Example |
|------|-------|---------|
| Org Secret | `${{ secrets.NAME }}` | `secrets.DOCKERHUB_TOKEN` |
| Org Variable | `${{ vars.NAME }}` | `vars.DOCKERHUB_USERNAME` |
| Repo Secret | `${{ secrets.NAME }}` | Also works if not set at org level |

### Troubleshooting

If login fails:
1. Check token is valid at https://hub.docker.com/settings/security
2. Verify username matches your Docker Hub account
3. Check org-level variable is set correctly