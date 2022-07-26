from pydantic import BaseModel
from typing import Optional, Literal

class ValidClaim(BaseModel):
    def __init__(self, *args, **kwargs):
        kwargs = {k.lower(): (None if v == "" else v) for k, v in kwargs.items()}
        super(ValidClaim, self).__init__(*args, **kwargs)

    calculated_patient_pay_amt: Optional[str] = None
    client_disp_fee_paid: Optional[str] = None
    client_ing_cost: Optional[str] = None
    admin_fee: Optional[str] = None
    total_reward: Optional[str] = None
    rewards: Optional[str] = None
    response_transaction_response_status: Optional[str] = None
    client_patient_sales_tax_amount_paid: Optional[str] = None
    client_plan_sales_tax_amount_paid: Optional[str] = None
    response_patient_sales_tax_amount: Optional[str] = None
    stocking_fee: Optional[str] = None
    client_employee_paid: Optional[str] = None
    client_employer_cost: Optional[str] = None
    updatedate: Optional[str] = None
    type: Optional[str] = None
    claim_status: Optional[str] = None
    transferresponse_version: Optional[str] = None
    transferresponse_transaction_response_status: Optional[str] = None
    transferresponse_transaction_count: Optional[str] = None
    transferresponse_transaction_code: Optional[str] = None
    transferresponse_service_provider_id_qualifier: Optional[str] = None
    transferresponse_service_provider_id: Optional[str] = None
    transferresponse_reject_count: Optional[str] = None
    transferresponse_reject_code: Optional[str] = None
    transferresponse_prescription_ref_num: Optional[str] = None
    transferresponse_prescription_number_qualifier: Optional[str] = None
    transferresponse_message: Optional[str] = None
    transferresponse_date_of_service: Optional[str] = None
    transferresponse_authorization_number: Optional[str] = None
    transferresponse_additional_message_information: Optional[str] = None
    transferrequest_processor_control_number: Optional[str] = None
    transferrequest_bin_number: Optional[str] = None
    transactionid: Optional[str] = None
    startdate: Optional[str] = None
    sequencenumber: Optional[int] = None
    response_version: Optional[str] = None
    response_url: Optional[str] = None
    response_transaction_count: Optional[str] = None
    response_transaction_code: Optional[str] = None
    response_total_amount_paid: Optional[str] = None
    response_pharmacy_payment_due: Optional[str] = None
    response_tax_exempt_indicator: Optional[str] = None
    response_service_provider_id_qualifier: Optional[str] = None
    response_service_provider_id: Optional[str] = None
    response_response_status: Optional[str] = None
    response_reject_field_occurrence_indicator: Optional[str] = None
    response_reject_count: Optional[str] = None
    response_reject_code: Optional[str] = None
    response_product_incentive: Optional[str] = None
    response_product_id_qualifier: Optional[str] = None
    response_product_id: Optional[str] = None
    response_product_description: Optional[str] = None
    response_product_count: Optional[str] = None
    response_product_cost_share_incentive: Optional[str] = None
    response_prescription_reference_number_qualifier: Optional[str] = None
    response_prescription_reference_number: Optional[str] = None
    response_plan_id: Optional[str] = None
    response_payer_id_qualifier: Optional[str] = None
    response_payer_id: Optional[str] = None
    response_patient_pay_amount: Optional[str] = None
    response_other_amount_paid_qualifier: Optional[str] = None
    response_other_amount_paid_count: Optional[str] = None
    response_other_amount_paid: Optional[str] = None
    response_network_reimbursement_id: Optional[str] = None
    response_message: Optional[str] = None
    response_ingredient_cost_paid: Optional[str] = None
    response_help_desk_phone_number_qualifier: Optional[str] = None
    response_help_desk_phone_number: Optional[str] = None
    response_group_id: Optional[str] = None
    response_flat_sales_tax_amount_paid: Optional[float] = None
    response_dispensing_fee_paid: Optional[str] = None
    response_date_of_service: Optional[str] = None
    response_date_of_birth: Optional[str] = None
    response_cardholder_id: Optional[str] = None
    response_basis_of_reimbursement_determination: Optional[str] = None
    response_authorization_number: Optional[str] = None
    response_amount_of_copay: Optional[str] = None
    response_amount_attributed_to_sales_tax: Optional[str] = None
    response_additional_message_information_qualifier: Optional[str] = None
    response_additional_message_information_count: Optional[str] = None
    response_additional_message_information_continuity: Optional[str] = None
    response_additional_message_information: Optional[str] = None
    request_version: Optional[str] = None
    request_usual_and_customary_charge: Optional[str] = None
    request_unit_of_measure: Optional[str] = None
    request_transaction_count: Optional[str] = None
    request_transaction_code: Optional[str] = None
    request_submission_clarification_code_count: Optional[str] = None
    request_submission_clarification_code: Optional[str] = None
    request_special_packaging_indicator: Optional[str] = None
    request_software_vendor: Optional[str] = None
    request_service_provider_id_qualifier: Optional[str] = None
    request_service_provider_id: Optional[str] = None
    request_scheduled_prescription_id_number: Optional[str] = None
    request_route_of_administration: Optional[str] = None
    request_quantity_intended_dispensed: Optional[str] = None
    request_quantity_dispensed: Optional[str] = None
    request_provider_accept_assignment_indicator: Optional[str] = None
    request_product_selection_code: Optional[str] = None
    request_product_id_qualifier: Optional[str] = None
    request_product_id: Optional[str] = None
    request_processor_control_number: Optional[str] = None
    request_procedure_modifier_code_count: Optional[str] = None
    request_procedure_modifier_code: Optional[str] = None
    request_prior_authorization_type_code: Optional[str] = None
    request_prior_authorization_number_submitted: Optional[str] = None
    request_primary_care_provider_last_name: Optional[str] = None
    request_primary_care_provider_id_qualifier: Optional[str] = None
    request_primary_care_provider_id: Optional[str] = None
    request_prescription_reference_number_qualifier: Optional[str] = None
    request_prescription_reference_number: Optional[str] = None
    request_prescription_origin_code: Optional[str] = None
    request_prescriber_zip_code: Optional[str] = None
    request_prescriber_street_address: Optional[str] = None
    request_prescriber_state_address: Optional[str] = None
    request_prescriber_phone_number: Optional[str] = None
    request_prescriber_last_name: Optional[str] = None
    request_prescriber_id_qualifier: Optional[str] = None
    request_prescriber_id: Optional[str] = None
    request_prescriber_first_name: Optional[str] = None
    request_prescriber_city_address: Optional[str] = None
    request_pregnancy_indicator: Optional[str] = None
    request_plan_id: Optional[str] = None
    request_place_of_service: Optional[str] = None
    request_pharmacy_service_type: Optional[str] = None
    request_person_code: Optional[str] = None
    request_percentage_sales_tax_rate_submitted: Optional[str] = None
    request_percentage_sales_tax_basis_submitted: Optional[str] = None
    request_percentage_sales_tax_amount_submitted: Optional[str] = None
    request_payment_count: Optional[str] = None
    request_patient_relationship_code: Optional[str] = None
    request_patient_paid_amount_submitted: Optional[str] = None
    request_patient_id_qualifier: Optional[str] = None
    request_patient_id: Optional[str] = None
    request_patient_gender_code: Optional[str] = None
    request_patient_assignment_indicator: Optional[str] = None
    request_other_payer_reject_count: Optional[str] = None
    request_other_payer_reject_code: Optional[str] = None
    request_other_payer_patient_responsibility_amount_qualifier: Optional[str] = None
    request_other_payer_patient_responsibility_amount_count: Optional[str] = None
    request_other_payer_patient_responsibility_amount: Optional[str] = None
    request_other_payer_id_qualifier: Optional[str] = None
    request_other_payer_id: Optional[str] = None
    request_other_payer_date: Optional[str] = None
    request_other_payer_coverage_type: Optional[str] = None
    request_other_payer_amount_paid_qualifier: Optional[str] = None
    request_other_payer_amount_paid_count: Optional[str] = None
    request_other_payer_amount_paid: Optional[str] = None
    request_other_coverage_code: Optional[str] = None
    request_other_amount_claimed_submitted_qualifier: Optional[str] = None
    request_other_amount_claimed_submitted_count: Optional[str] = None
    request_other_amount_claimed_submitted: Optional[str] = None
    request_originally_prescribed_quantity: Optional[str] = None
    request_originally_prescribed_product_id_qualifier: Optional[str] = None
    request_originally_prescribed_product_code: Optional[str] = None
    request_number_of_refills_authorized: Optional[str] = None
    request_medigap_id: Optional[str] = None
    request_medicaid_indicator: Optional[str] = None
    request_medicaid_id_number: Optional[str] = None
    request_level_of_service: Optional[str] = None
    request_internal_control_number: Optional[str] = None
    request_intermediary_authorization_type_id: Optional[str] = None
    request_intermediary_authorization_id: Optional[str] = None
    request_ingredient_cost_submitted: Optional[str] = None
    request_ingredient_component_count: Optional[str] = None
    request_incentive_amount_submitted: Optional[str] = None
    request_home_plan: Optional[str] = None
    request_group_id: Optional[str] = None
    request_gross_amount_due: Optional[str] = None
    request_gpi: Optional[str] = None
    request_flat_sales_tax_amount_submitted: Optional[str] = None
    request_fill_number: Optional[str] = None
    request_employer_id: Optional[str] = None
    request_eligibility_clarification_code: Optional[str] = None
    request_dispensing_status: Optional[str] = None
    request_dispensing_fee_submitted: Optional[float] = None
    request_delay_reason_code: Optional[str] = None
    request_days_supply_intended_dispensed: Optional[str] = None
    request_days_supply: Optional[str] = None
    request_date_prescription_written: Optional[str] = None
    request_date_of_service: Optional[str] = None
    request_date_of_birth: Optional[str] = None
    request_compound_type: Optional[str] = None
    request_compound_ingredients: str = "[]"
    request_compound_code: Optional[str] = None
    request_cms_part_d_defined_qualified_facility: Optional[str] = None
    request_cardholder_id: Optional[str] = None
    request_bin_number: Optional[str] = None
    request_benefit_stage_qualifier: Optional[str] = None
    request_benefit_stage_count: Optional[str] = None
    request_benefit_stage_amount: Optional[str] = None
    request_basis_of_cost_determination: Optional[str] = None
    request_associated_prescription_reference_number: Optional[str] = None
    request_associated_prescription_date: Optional[str] = None
    prescription_id: Optional[str] = None
    overridenumber: Optional[str] = None
    override_thru: Optional[str] = None
    override_percentage: Optional[str] = None
    override_from: Optional[str] = None
    override_amount: Optional[str] = None
    over_ride: Optional[str] = None
    enddate: Optional[str] = None
    createdate: Optional[str] = None
    copay_override: Optional[str] = None
    autoerx_failure_reason: Optional[str] = None
    auth_id: Optional[str] = None
    calculated_drug_cost: Optional[str] = None
    calculated_disp_fee: Optional[str] = None
    calculated_employer_cost: Optional[str] = None
    calculated_ing_cost: Optional[str] = None
    rebate_amount: Optional[str] = None
    submitted_ing_cost: Optional[str] = None
    unit_price: Optional[str] = None
    unit_price_before_rebate: Optional[float] = None
    unc_ing_cost: Optional[str] = None
    alternative_drug_rewards: Optional[str] = None
    brand_generic: Optional[str] = None
    pa_flag: Optional[str] = None
    price_type: Optional[str] = None
    default_payment_option: Optional[str] = None
    pharmacy_dispensing_fee: Optional[str] = None
    claims_processor: Optional[str] = None
    submitted_disp_fee: Optional[str] = None
    copay_type: Optional[str] = None
    package_quantity: Optional[str] = None
    submitted_drug_cost: Optional[str] = None
    coverage_tier_name: Optional[str] = None
    copay: Optional[str] = None
    drug_dosage: Optional[str] = None
    awp_unit_price: Optional[str] = None
    alternate_penalty: Optional[str] = None
    submitted_patient_paid_amount: Optional[str] = None
    rebate_factor: Optional[str] = None
    manufacturer_name: Optional[str] = None
    drug_manufacturer: Optional[str] = None
    drug_strength: Optional[str] = None
    payer_dispensing_fee: Optional[float] = None
    plan_year: Optional[str] = None
    group_type: Optional[str] = None
    reward_share: Optional[str] = None
    payer_sales_tax: Optional[float] = None
    reward_percentage: Optional[str] = None
    retail_reward: Optional[str] = None
    awp_amount: Optional[str] = None
    baseline_cost: Optional[str] = None
    payer_authid: Optional[str] = None
    deductible_accumulator_amount: Optional[str] = None
    payer_patient_paid_amount: Optional[float] = None
    client_drug_cost_paid: Optional[str] = None
    pharmacy_name: Optional[str] = None
    unc_employer_cost: Optional[str] = None
    otc_indicator: Optional[str] = None
    submitted_total_amount: Optional[str] = None
    drug_penalty: Optional[str] = None
    pharmacy_chain_code: Optional[str] = None
    benefit_plan_name: Optional[str] = None
    calculated_employee_opc: Optional[str] = None
    unc_drug_cost: Optional[str] = None
    drug_name: Optional[str] = None
    opc_remaining: Optional[str] = None
    payer_ing_cost: Optional[float] = None
    gppc: Optional[str] = None
    client_deductible: Optional[str] = None
    package_size: Optional[str] = None
    domain: Optional[str] = None
    mail_retail_code: Optional[str] = None
    pharmacy_type: Optional[str] = None
    tpa_member_id: Optional[str] = None
    oop_accumulator_amount: Optional[str] = None
    employee_opc: Optional[str] = None
    unc_disp_fee: Optional[str] = None
    copay_amt: Optional[str] = None
    multi_source: Optional[str] = None
    unc_patient_paid_amount: Optional[str] = None
    member_group: Optional[str] = None
    submitted_employer_cost: Optional[str] = None
    payer_client_due_amt: Optional[float] = None
    rx_flipt_person_id: Optional[str] = None
    employee_id: Optional[str] = None
    specialty_flag: Optional[str] = None
    member_choice_penalty_amount: Optional[str] = None
    payer_sequence_number: Optional[str] = None
    erx_status: Optional[str] = None
    payee_type: Optional[str] = None
    deductible_accumulator_flag: Optional[Literal['Y', 'N']] = None
    oop_accumulator_flag: Optional[Literal['Y', 'N']] = None
    incentive_credit_applied: Optional[str] = None
    incentive_credit_remaining: Optional[str] = None
    process_error_code: Optional[str] = None
    rds_subsidy_determination_indicator: Optional[str] = None
    medicare_type: Optional[str] = None
    etl_status: str = None


class InvalidClaim(ValidClaim):
    calculated_patient_pay_amt: str
    client_disp_fee_paid: str
    client_ing_cost: str
    client_patient_sales_tax_amount_paid: str
    client_plan_sales_tax_amount_paid: str
    response_patient_sales_tax_amount: str
    client_employee_paid: str
    client_employer_cost: str
    claim_status: str = "P"
    transactionid: str
    startdate: str
    sequencenumber: int
    request_quantity_dispensed: str
    request_product_id: str
    request_service_provider_id: str
    request_prescription_reference_number: str
    request_prescriber_id: str
    request_fill_number: str
    request_days_supply: str
    request_date_prescription_written: str
    request_date_of_service: str
    request_compound_ingredients: str = "[]"
    auth_id: str
    pa_flag: Literal['N', 'Y']
    domain: str
    rx_flipt_person_id: str
    erx_status: str = "P"
    etl_status: str = None