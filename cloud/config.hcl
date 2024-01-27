locals {
  organization = "logikal.io"
  project = "django"
  backend = "gcs"

  providers = {
    random = {
      version = "~> 3.6"
    }
    google = {
      version = "~> 5.9"
      region = "europe-west6"
    }
    aws = {
      version = "~> 5.31"
      region = "eu-central-2"
    }
    dnsimple = {
      version = "~> 1.3"
    }
  }
}
