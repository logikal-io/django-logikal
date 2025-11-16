include "commons" {
  path = pathexpand("~/.terragrunt/commons.hcl")
  expose = true
}

inputs = {
  organization_id = include.commons.locals.organization_id
}
