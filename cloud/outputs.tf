output "gcp_testing_workload_identity_provider" {
  value = module.gcp_github_auth.workload_identity_provider
}

output "gcp_testing_service_account" {
  value = module.gcp_github_auth.service_account_emails["testing"]
}
