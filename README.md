# EOI Master - FastAPI 

## How to run with Docker Compose
### Development
- Redis data in kv/data
- Set to build images
- Includes httpd for performance test
1. Run `docker-compose up -d`

### Production: docker-compose-prod.yml
- No Redis data
- Pulls images from DockerHub
1. Run `docker-compose -f docker-compose-prod.yml up -d`