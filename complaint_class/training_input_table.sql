%sql
 insert overwrite spark_catalog.gms_us_mart.nlpcc_prediction_model_training_data
 select 
 grid_tbl_1.*,
 comp_tbl_1.PQC, comp_tbl_1.INT, comp_tbl_1.Country_of_Origin, comp_tbl_1.Awareness_Date, comp_tbl_1.product_family_gcms as Product_Family_GCMS, comp_tbl_1.Status_Name, comp_tbl_1.date_closed as Date_Closed, CASE when comp_tbl_1.date_closed is not null then '1' else '0' end as is_closed
 ,comp_tbl_1.Initial_Classification, comp_tbl_1.Final_Classification, `Complaint Description` as Complaint_Description
 from 
 (SELECT
 Pr_id,
 nullif(array_join(collect_list(distinct AE), '; '), '') as AE,
 nullif(array_join(collect_list(distinct Lot_Number), '; '), '') as Lot_Number_Gd,
 nullif(array_join(collect_list(distinct Vendor_Lot_Number), '; '), '') as Vendor_Lot_Number,
 nullif(array_join(collect_list(distinct First_Name), '; '), '') as  First_Name, 
 nullif(array_join(collect_list(distinct Last_Name), '; '), '') as Last_Name,
 nullif(array_join(collect_list(distinct Reference_Number), '; '), '') as Reference_Number,
 nullif(array_join(collect_list(distinct Material_Details), '; '), '') as Material_Details,
 nullif(array_join(collect_list(distinct Final_SubCategory), '; '), '') as Final_SubCategory,
 nullif(array_join(collect_list(distinct Final_Category), '; '), '') as Final_Category

 FROM (SELECT pr_id as Pr_id, seq_no, 
 grid_field_nm, grid_field_value
 from GMS_US_MART.REF_grid_data_detail_TRKW_GLBL 
 where 
   grid_nm = 'AE #' or
   grid_nm = 'Affected Lot' or
   grid_nm = 'Category Grid' or
   grid_nm = 'Contact Information' or
   grid_nm = 'Lot Genealogy Grid' or
   grid_nm = 'R&D / Clinical Supplier' or
   grid_nm = 'Record Cross Reference' or
   grid_nm = 'Supplier/Site'
 )
 PIVOT (MIN(grid_field_value) FOR grid_field_nm IN (
  'AE #^' as AE, 'AE Description^' as AE_Description, 'Customer Lot #' as Customer_Lot_Number, 'Lot#' as Lot_Number, 'Vendor Lot #' as Vendor_Lot_Number, 'Material Desc' as Material_Description, 'Material Code' as Material_Code, 'Material Details' as Material_Details, 'Expiry Date' as Expiry_Date, 'Plant' as Plant, 'Initial SubCategory^' as Initial_SubCategory, 'Final SubCategory^' as Final_SubCategory, 'Final Category^' as Final_Category, 'Initial Category^' as Initial_Category, 'Country^' as Country, 'Facility Name^' as Facility_Name, 'First Name^' as First_Name, 'Last Name^' as Last_Name, 'Primary Contact^' as Primary_Contact, 'Drug Product^' as Drug_Product, 'Finished Goods Lot Number^' as Finished_Good_Lot_Number, 'Drug Substance^' as Drug_Substance, 'External Reference Number^' as Extenal_Reference_Number, 'Name^' as Name, 'Reference Number^' as Reference_Number, 'Reference Type^' as Reference_Type, 'Supplier Contact^' as Supplier_Contact, 'Supplier/Site Complaint^' as Supplier_Site_Complaint, 'Supplier/Site Info^' as Supplier_Site_Info, 'Date Investigation Received^' as Date_Investigation_Received
 )
 )
 group by Pr_id
 )as grid_tbl_1

 left outer join  

 (select * from gms_us_mart.txn_complaint_record_trkw_glbl) as comp_tbl_1
 on grid_tbl_1.Pr_id = comp_tbl_1.pr_id 

 Left join (
     select * from 
 (select pe.PR_ID as pr_id, df.name as FIELD_NAME, pe.TEXT
 From (Select *, rank() over (partition by PR_ID, PR_ELEMENT_TYPE order by ID desc) rnk From GMS_US_LAKE.gmsgq_trackwise_pr_element) pe 
   join GMS_US_LAKE.gmsgq_trackwise_data_fields df on pe.pr_element_type=df.pr_element_type
   join GMS_US_LAKE.gmsgq_trackwise_pr          pr on pe.pr_id=pr.id
   join GMS_US_LAKE.gmsgq_trackwise_project     pj on pr.PROJECT_ID=pj.id
 Where pe.active_flag='Y' and pe.rnk=1 and pr.status_type<>408 and pr.PROJECT_ID=51)

 Pivot (min(text) for field_name in ('Complaint Description', 'Closure Summary'))
   ) 
   b on grid_tbl_1.Pr_id = b.pr_id

 where
 comp_tbl_1.aud_ld_dts = (
     select max(aud_ld_dts)
     from gms_us_mart.txn_complaint_record_trkw_glbl
 )  
