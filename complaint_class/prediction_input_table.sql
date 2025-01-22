%sql
 insert overwrite gms_us_mart.nlpcc_prediction_data_input

 select tbl1.Pr_id, tbl1.Complaint_Description, tbl2.Status_Name from
 (select * from
 (select pe.PR_ID as Pr_id, df.name as FIELD_NAME, pe.TEXT
 From (Select *, rank() over (partition by PR_ID, PR_ELEMENT_TYPE order by ID desc) rnk From GMS_US_LAKE.gmsgq_trackwise_pr_element) pe 
   join GMS_US_LAKE.gmsgq_trackwise_data_fields df on pe.pr_element_type=df.pr_element_type
   join GMS_US_LAKE.gmsgq_trackwise_pr          pr on pe.pr_id=pr.id
   join GMS_US_LAKE.gmsgq_trackwise_project     pj on pr.PROJECT_ID=pj.id
 Where pe.active_flag='Y' and pe.rnk=1 and pr.status_type<>408 and pr.PROJECT_ID=51)
 Pivot (min(text) for field_name in ('Complaint Description' as Complaint_Description))) tbl1
 join

 (
   SELECT
   T1.pr_id,
   T1.Status_Name
 FROM
   (
     Select
       CAST (`pr_id` AS string) AS pr_id,
       CAST (`Status_Name` AS string) AS Status_Name
     from(
         WITH MAIN_PR AS (
           SELECT
             
             CAST(PR.PR_ID AS BIGINT) AS PR_ID,
             CAST(PR.PROJ_ID_FK AS BIGINT) AS PROJ_ID,
             CAST(PR.STAT_TYPE_ID_FK AS BIGINT) AS STAT_TYP,
             ST.STAT_TYPE_NM AS STAT_NM
             FROM
             GMS_US_HUB.TXN_PR_TRKW_GLBL PR
             LEFT JOIN (
               SELECT
                 SN.PR_ID_FK,
                 MIN(SN.START_DTS) AS ORIGINAL_CLOSED_DT
               FROM
                 GMS_US_HUB.TXN_PR_TRKW_GLBL PR
                 LEFT JOIN GMS_US_HUB.TXN_PR_STATE_NODE_TRKW_GLBL SN ON SN.PR_ID_FK = PR.PR_ID
                 AND SN.ACTIVE_FLAG = 'Y'
                 JOIN GMS_US_HUB.REF_PR_STATUS_TYPE_TRKW_GLBL PST ON SN.PR_STAT_TYPE_ID_FK = PST.STAT_ID
               WHERE
                 PR.ACTIVE_FLAG = 'Y'
                 AND PST.ACTIVE_FLAG = 'Y'
                 AND PST.CLOSED_FLG = 1
                 AND (
                   PST.STAT_ID <> 51
                   OR SN.END_DTS IS NULL
                 )
               GROUP BY
                 SN.PR_ID_FK
             ) A ON PR.PR_ID = A.PR_ID_FK
             JOIN GMS_US_HUB.REF_PROJECT_TRKW_GLBL PROJ ON PR.PROJ_ID_FK = PROJ.PROJ_ID
             JOIN GMS_US_HUB.REF_PR_STATUS_TYPE_TRKW_GLBL ST ON PR.STAT_TYPE_ID_FK = ST.STAT_ID
             JOIN GMS_US_HUB.REF_PROCESS_GROUP_TRKW_GLBL PG ON PROJ.PROC_GRP_ID = PG.PROC_GRP_ID
             LEFT JOIN GMS_US_HUB.REF_PERSON_RELATIONSHIP_TRKW_GLBL ORIG ON PR.ORIGIN_REL_ID = ORIG.PERSON_REL_ID
             AND ORIG.ACTIVE_FLAG = 'Y'
             LEFT JOIN GMS_US_HUB.REF_LOGIN_INFO_TRKW_GLBL LOGIN ON PR.RESP_REL_ID = LOGIN.PERSON_REL_ID
 												  
             AND LOGIN.ACTIVE_FLAG = 'Y'
             LEFT JOIN GMS_US_HUB.REF_PERSON_RELATIONSHIP_TRKW_GLBL RESP ON PR.RESP_REL_ID = RESP.PERSON_REL_ID
             AND RESP.ACTIVE_FLAG = 'Y'
             LEFT JOIN GMS_US_HUB.REF_ADDRESS_TRKW_GLBL ADDRESS ON RESP.PERSON_ADDRESS_ID = ADDRESS.ADDR_ID
             AND ADDRESS.ACTIVE_FLAG = 'Y'
           WHERE
             PROJ.ACTIVE_FLAG = 'Y'
             AND ST.ACTIVE_FLAG = 'Y'
             AND PG.ACTIVE_FLAG = 'Y'
             AND PR.STAT_TYPE_ID_FK <> 408
         ),
         MAIN_ADDTL_DATA AS (
           SELECT
             
             PRD.PR_ADDTL_DATA_ID AS PR_ADDTL_DATA_ID,
             PRD.PR_ID_FK AS PR_ID,
             PRD.DATA_FIELD_ID_FK AS DATA_FIELD_ID,
             DF.DATA_FIELD_NM AS DATA_FIELD_NM,
             DF.FIELD_CLASS_ID AS FIELD_CLASS ,CASE
               WHEN FIELD_CLASS_ID IN (1, 13) THEN (
                 SELECT
                   MAX(ADDTL_TYPE_NM)
                 FROM
                   GMS_US_HUB.REF_ADDTL_TYPE_TRKW_GLBL
                 WHERE
                   ADDTL_TYPE_ID = PRD.NUM_VAL
                   AND ACTIVE_FLAG = 'Y'
               )
               WHEN FIELD_CLASS_ID IN (3, 21) THEN CAST(PRD.NUM_VAL AS BIGINT)
               WHEN FIELD_CLASS_ID IN (7, 16) THEN (
                 SELECT
                   MAX(PERSON_NM)
                 FROM
                   GMS_US_HUB.REF_PERSON_RELATIONSHIP_TRKW_GLBL
                 WHERE
                   PERSON_REL_ID = PRD.NUM_VAL
                   AND ACTIVE_FLAG = 'Y'
               )
               WHEN FIELD_CLASS_ID IN (8, 20) THEN (
                 SELECT
                   MAX(ENTITY_NM)
                 FROM
                   GMS_US_HUB.REF_ENTITY_TRKW_GLBL
                 WHERE
                   ENTITY_ID = PRD.NUM_VAL
                   AND ACTIVE_FLAG = 'Y'
               )
               WHEN FIELD_CLASS_ID = 5 THEN LEFT(VAL_DT, 10)
               WHEN FIELD_CLASS_ID = 4 THEN CAST(DEC_VAL AS DOUBLE)
               WHEN FIELD_CLASS_ID = 6 THEN VAL_DTS
               ELSE TRIM(PRD.S_VAL)
             END AS FIELD_VALUE
           FROM
             GMS_US_HUB.TXN_PR_ADDITIONAL_DATA_TRKW_GLBL PRD
             JOIN GMS_US_HUB.REF_DATA_FIELDS_INFO_TRKW_GLBL DF ON PRD.DATA_FIELD_ID_FK = DF.DATA_FIELD_ID
           WHERE
             PRD.ACTIVE_FLAG = 'Y'
             AND DF.ACTIVE_FLAG = 'Y'
         )
         select
           pr.pr_id,
           pr.stat_nm as Status_Name,
           ad.field_value,
           ad.data_field_nm
         from
           MAIN_PR pr
           Join (MAIN_ADDTL_DATA) ad on pr.pr_id = ad.pr_id
           and pr.proj_id = 51
           Left Join (
             Select
               pr_id,
               concat_ws(
                 '; ',
                 collect_list(trim(substring_index(field_value, '\\', -1)))
               ) AS `Attachments`
             FROM
               (MAIN_ADDTL_DATA)
             WHERE
               data_field_nm = 'Attachments'
             GROUP BY
               pr_id
           ) t1 on pr.pr_id = t1.pr_id
       ) PIVOT (
         concat_ws('; ', collect_set(field_value)) for data_field_nm in (
           'Approved Extensions', 'As Determined Problem Code', 'Associated AE', 'Australia Reportability', 'Batch Review Q1', 'Brazil Reportability', 'CA Reportability', 'Cause Code', 'Clinical Study Affected?', 'CMB Impacted?', 'Complaint Confirmed?', 'Complaint Init. Timeliness', 'Complaint Type', 'Conditional /Event Initiated', 'Conditional /Post Market Es.', 'Country of Origin', 'Customer Response Requested?', 'Due Diligence Complete?', 'EU Impact', 'EU Reportability', 'Event/CAPA Initiated?', 'Extension Request #', 'Final Classification', 'Final Release Facility', 'Initial Classification', 'Is Assess. Reportability Req.?', 'Is Sample Available?', 'Issue Escalation?', 'Japan Reportability', 'Late Complaint', 'Manufacturing Evaluation Type?', 'Manufacturing Facility', 'Market Research', 'Missed Target Date Rationale', 'Operational Unit', 'Other Reportability', 'Owning Dept.', 'Owning Group', 'Patient Received Dose?', 'Patient or User Injury?', 'Product Family (GCMS)', 'Product Group', 'Reg Ag. Notif. by Complainant?', 'Sample Evaluation Q1', 'Sample Evaluation Q2', 'Sample Requested?', 'Sent to/Rec. From Drug Safety?', 'Source System', 'Third Party Notification Sent', 'Trend Identified?', 'US Reportability', 'Was Customer Response Perf.?', 'Complaint Initiation Comment', 'Complaint Trend Comments', 'Confirmed Complaint Comments', 'Customer Response Performed By', 'Email Address', 'Escalation #', 'INT #', 'Lot Number', 'Missed Target Date Comment', 'PQC #', 'Postal Code', 'Product Code/Description', 'Rationale if No Escalation', 'Rationale if No Event/CAPA', 'Sample Received By', 'State/Province', 'Title (English)', 'Unique Device Identifier', 'Vendor Batch No', 'Version Number', 'Quantity', 'Sample Quantity', 'AE Identification Date', 'Awareness Date', 'Expiration Date', 'GDS Notification Date', 'Occurrence Date', 'Sample Received Date', 'Submission Date', 'Target Closure Date' as Target_Date, 'Complaint Cancellation Req. on', 'Eval. & eMDR Compl. on', 'Eval. Assignment/DT Compl. on', 'Evaluation Initiated on', 'Ready for Close on', 'Rejected On', 'Submitted for Mgmt App. on', 'Submitted on', 'Approval for Close by', 'Approver', 'Canceled by', 'Cancellation Quality Approver', 'Clinical Complaint Owner', 'Closed by', 'Complaint Cancellation Req. by', 'Complaint Owner', 'Customer Response Assignee', 'Eval. & eMDR Compl. by', 'Eval. Assignment/DT Compl. by', 'Evaluation Initiated by', 'External Eval. Requested by', 'Previous Clinical CO', 'Previous Complaint Owner', 'Ready for Close by', 'Rejected By', 'Submitted by', 'SME Reviewer 1', 'SME Reviewer 2', 'SME Reviewer 3', 'Submitted for Mgmt App. by', 'Study Number', 'As Reported Problem Code', 'Cause Code - Tier II', 'Component Code', 'Notification Recipient(s)', 'Event/CAPA Opened for Compl.', 'Related Complaint PR#(s)', 'CMB Impacted Name', 'Related Event/CAPA', 'Trackwise Reference Record'
           
         )
       )
   ) T1

 )tbl2

 on tbl1.Pr_id = tbl2.pr_id
 where tbl2.Status_Name = "Opened" or  tbl2.Status_Name = "Complaint Determination"