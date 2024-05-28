module "kubernetes" {
  source                        = "/home/lucas/Documents/Workspace/aws-eks-cluster"
  cidr_block                    = "10.0.0.0/16"
  project_name                  = "parking-devops"
  region                        = "us-east-1"
  github_account_and_repository = "lucasfacci/parking-devops"
  github_repository_branch_name = "main"
  tags = {
    "Department" = "DevOps"
  }
}
