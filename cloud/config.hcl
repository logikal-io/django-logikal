locals {
  state_backend = "gcs"
  organization = "logikal.io"
  project = "django"

  providers = {
    random = {
      version = "~> 3.7"
    }
    google = {
      version = "~> 7.11"
      region = "europe-west6"
    }
    aws = {
      version = "~> 6.21"
      region = "eu-central-2"
    }
    dnsimple = {
      version = "~> 1.10"
    }
  }
}
