locals {
  organization = "logikal.io"
  project = "django"
  backend = "gcs"

  providers = {
    google = {
      version = "~> 4.52"
      region = "europe-west6"
    }
    aws = {
      version = "~> 4.41"
      region = "eu-central-2"
    }
    dnsimple = {
      version = "~> 0.14"
    }
  }
}
