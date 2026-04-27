# Services
resource "google_project_service" "secret_manager" {
  service = "secretmanager.googleapis.com"
}

resource "google_project_service" "logging" {
  service = "logging.googleapis.com"
}

# Secrets
resource "random_password" "secret_key" {
  length = 50
}

resource "google_secret_manager_secret" "secret_key" {
  secret_id = "django-logikal-secret-key"
  replication {
    auto {}
  }

  depends_on = [google_project_service.secret_manager]
}

resource "google_secret_manager_secret_version" "secret_key" {
  secret = google_secret_manager_secret.secret_key.id
  secret_data = random_password.secret_key.result
}

locals {
  providers = ["google", "apple", "microsoft"]
}

resource "google_secret_manager_secret" "auth_secret" {
  for_each = toset(local.providers)

  secret_id = "django-logikal-auth-secret-${each.value}"
  replication {
    auto {}
  }

  depends_on = [google_project_service.secret_manager]
}

# Emailing
resource "aws_ses_domain_identity" "django_logikal_org" {
  domain = "django-logikal.org"
}

resource "aws_ses_domain_dkim" "django_logikal_org" {
  domain = aws_ses_domain_identity.django_logikal_org.domain
}

data "google_dns_managed_zone" "django_logikal_org" {
  name = "django-logikal-org"
}

resource "google_dns_record_set" "django_logikal_org_dkim" {
  for_each = toset(aws_ses_domain_dkim.django_logikal_org.dkim_tokens)

  name = "${each.key}._domainkey.django-logikal.org."
  type = "CNAME"
  ttl = 3600

  managed_zone = data.google_dns_managed_zone.django_logikal_org.name

  rrdatas = ["${each.key}.dkim.eu-central-2.amazonses.com."]
}
