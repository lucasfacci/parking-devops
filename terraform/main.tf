module "kubernetes" {
  source       = "git@github.com:lucasfacci/aws-eks-cluster.git?ref=main"
  cidr_block   = "10.0.0.0/16"
  project_name = "parking-devops"
  region       = "us-east-1"
  tags = {
    "Department" = "DevOps"
  }
}
