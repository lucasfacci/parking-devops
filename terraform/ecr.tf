resource "aws_ecr_repository" "ecr" {
  name         = "parking-devops-api"
  force_delete = true
}