# Services
resource "google_project_service" "secret_manager" {
  service = "secretmanager.googleapis.com"
}

resource "google_project_service" "logging" {
  service = "logging.googleapis.com"
}

# Django secrets
resource "random_password" "django_secret_key" {
  length = 50
}

resource "google_secret_manager_secret" "django_secret_key" {
  secret_id = "django-secret-key"
  replication {
    automatic = true
  }

  depends_on = [google_project_service.secret_manager]
}

resource "google_secret_manager_secret_version" "django_secret_key" {
  secret = google_secret_manager_secret.django_secret_key.id
  secret_data = random_password.django_secret_key.result
}

# Emailing
provider "aws" {
  profile = var.organization_id
  region = "eu-central-1"  # SES is not available in eu-central-2 yet
  alias = "eu_central_1"
}

resource "aws_ses_domain_identity" "django_logikal_org" {
  provider = aws.eu_central_1

  domain = "django-logikal.org"
}

resource "aws_ses_domain_dkim" "django_logikal_org" {
  provider = aws.eu_central_1

  domain = aws_ses_domain_identity.django_logikal_org.domain
}

resource "dnsimple_zone_record" "docs_website" {
  for_each = toset(aws_ses_domain_dkim.django_logikal_org.dkim_tokens)

  zone_name = aws_ses_domain_identity.django_logikal_org.domain
  name = "${each.key}._domainkey"
  value = "${each.key}.dkim.amazonses.com"
  type = "CNAME"
  ttl = 3600
}
