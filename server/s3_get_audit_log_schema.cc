/*
 * Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * For any questions about this software or licensing,
 * please email opensource@seagate.com or cortx-questions@seagate.com.
 *
 */

#include "s3_error_codes.h"
#include "s3_log.h"
#include "s3_api_handler.h"
#include "s3_get_audit_log_schema.h"

S3GetAuditLogSchema::S3GetAuditLogSchema(std::shared_ptr<S3RequestObject> req)
    : S3Action(req, true, nullptr, true, true), request(req) {
  schema = "abc";
  setup_steps();
}
S3GetAuditLogSchema::~S3GetAuditLogSchema() {
  s3_log(S3_LOG_DEBUG, "", "%s\n", __func__);
}
void S3GetAuditLogSchema::setup_steps() {
  set_string();
  send_response_to_s3_client();
}

void S3GetAuditLogSchema::set_string() { schema = "efgh"; }

void S3GetAuditLogSchema::send_response_to_s3_client() {

  request->set_out_header_value("csmschema", schema.c_str());
  request->send_response(S3HttpSuccess204);
}
