#!/usr/bin/env python3

#
#  fix obvious issues in a brownfield land CSV
#  -- make it valid according to the 2019 guidance
#  -- log fixes as suggestions for the user to amend
#


class Transformer:
    def __init__(self, fields, organisation={}):
        self.fields = fields

        # map of OrganisationURI to organisation CURIE
        self.organisation_curie = {}
        for org in organisation.values():
            if org.get("opendatacommunities", None):
                self.organisation_curie[org["opendatacommunities"]] = org[
                    "organisation"
                ]

    def transform(self, reader):

        for stream_data in reader:
            row = stream_data["row"]
            o = {}
            row["resource"] = stream_data["resource"]

            # translate OrganisationURI into an organisation CURIE
            if "OrganisationURI" in row:
                row["OrganisationURI"] = self.organisation_curie.get(
                    row["OrganisationURI"], ""
                )

            for field, source in self.fields.items():
                o[field] = row[source]

            yield {
                "resource": stream_data["resource"],
                "row": o,
            }
