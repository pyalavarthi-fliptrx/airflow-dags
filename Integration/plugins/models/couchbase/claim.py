from typing import List
from pydantic import BaseModel
from typing import Optional, Union, Literal

# COUCHBASE CLAIM INFO

class ClaimRequest(BaseModel):
    def __init__(self, *args, **kwargs):
        kwargs = {k: (None if v == "" else v) for k, v in kwargs.items()}
        super(ClaimRequest, self).__init__(*args, **kwargs)

    version: Optional[str] = None
    usual_and_customary_charge: Optional[str] = None
    unit_of_measure: Optional[str] = None
    transaction_count: Optional[str] = None
    transaction_code: Optional[str] = None
    submission_clarification_code_count: Optional[str] = None
    submission_clarification_code: Optional[str] = None
    special_packaging_indicator: Optional[str] = None
    software_vendor: Optional[str] = None
    service_provider_id_qualifier: Optional[str] = None
    service_provider_id: Optional[str] = None
    scheduled_prescription_id_number: Optional[str] = None
    route_of_administration: Optional[str] = None
    quantity_intended_dispensed: Optional[str] = None
    quantity_dispensed: Optional[str] = None
    provider_accept_assignment_indicator: Optional[str] = None
    product_selection_code: Optional[str] = None
    product_id_qualifier: Optional[str] = None
    product_id: Optional[str] = None
    processor_control_number: Optional[str] = None
    procedure_modifier_code_count: Optional[str] = None
    procedure_modifier_code: Optional[str] = None
    prior_authorization_type_code: Optional[str] = None
    prior_authorization_number_submitted: Optional[str] = None
    primary_care_provider_last_name: Optional[str] = None
    primary_care_provider_id_qualifier: Optional[str] = None
    primary_care_provider_id: Optional[str] = None
    prescription_reference_number_qualifier: Optional[str] = None
    prescription_reference_number: Optional[str] = None
    prescription_origin_code: Optional[str] = None
    prescriber_zip_code: Optional[str] = None
    prescriber_street_address: Optional[str] = None
    prescriber_state_address: Optional[str] = None
    prescriber_phone_number: Optional[str] = None
    prescriber_last_name: Optional[str] = None
    prescriber_id_qualifier: Optional[str] = None
    prescriber_id: Optional[str] = None
    prescriber_first_name: Optional[str] = None
    prescriber_city_address: Optional[str] = None
    pregnancy_indicator: Optional[str] = None
    plan_id: Optional[str] = None
    place_of_service: Optional[str] = None
    pharmacy_service_type: Optional[str] = None
    person_code: Optional[str] = None
    percentage_sales_tax_rate_submitted: Optional[str] = None
    percentage_sales_tax_basis_submitted: Optional[str] = None
    percentage_sales_tax_amount_submitted: Optional[str] = None
    payment_count: Optional[str] = None
    patient_relationship_code: Optional[str] = None
    patient_paid_amount_submitted: Optional[str] = None
    patient_id_qualifier: Optional[str] = None
    patient_id: Optional[str] = None
    patient_gender_code: Optional[str] = None
    patient_assignment_indicator: Optional[str] = None
    other_payer_reject_count: Optional[str] = None
    other_payer_reject_code: Optional[str] = None
    other_payer_patient_responsibility_amount_qualifier: Optional[str] = None
    other_payer_patient_responsibility_amount_count: Optional[str] = None
    other_payer_patient_responsibility_amount: Optional[str] = None
    other_payer_id_qualifier: Optional[str] = None
    other_payer_id: Optional[str] = None
    other_payer_date: Optional[str] = None
    other_payer_coverage_type: Optional[str] = None
    other_payer_amount_paid_qualifier: Optional[str] = None
    other_payer_amount_paid_count: Optional[str] = None
    other_payer_amount_paid: Optional[str] = None
    other_coverage_code: Optional[str] = None
    other_amount_claimed_submitted_qualifier: Optional[str] = None
    other_amount_claimed_submitted_count: Optional[str] = None
    other_amount_claimed_submitted: Optional[str] = None
    originally_prescribed_quantity: Optional[str] = None
    originally_prescribed_product_id_qualifier: Optional[str] = None
    originally_prescribed_product_code: Optional[str] = None
    number_of_refills_authorized: Optional[str] = None
    medigap_id: Optional[str] = None
    medicaid_indicator: Optional[str] = None
    medicaid_id_number: Optional[str] = None
    level_of_service: Optional[str] = None
    internal_control_number: Optional[str] = None
    intermediary_authorization_type_id: Optional[str] = None
    intermediary_authorization_id: Optional[str] = None
    ingredient_cost_submitted: Optional[str] = None
    ingredient_component_count: Optional[str] = None
    incentive_amount_submitted: Optional[str] = None
    home_plan: Optional[str] = None
    group_id: Optional[str] = None
    gross_amount_due: Optional[str] = None
    gpi: Optional[str] = None
    flat_sales_tax_amount_submitted: Optional[str] = None
    fill_number: Optional[str] = None
    employer_id: Optional[str] = None
    eligibility_clarification_code: Optional[str] = None
    dispensing_status: Optional[str] = None
    dispensing_fee_submitted: Optional[float] = None
    delay_reason_code: Optional[str] = None
    days_supply_intended_dispensed: Optional[str] = None
    days_supply: Optional[str] = None
    date_prescription_written: Optional[str] = None
    date_of_service: Optional[str] = None
    date_of_birth: Optional[str] = None
    compound_type: Optional[str] = None
    compound_ingredients: List = []
    compound_code: Optional[str] = None
    cms_part_d_defined_qualified_facility: Optional[str] = None
    cardholder_id: Optional[str] = None
    bin_number: Optional[str] = None
    benefit_stage_qualifier: Optional[str] = None
    benefit_stage_count: Optional[str] = None
    benefit_stage_amount: Optional[str] = None
    basis_of_cost_determination: Optional[str] = None
    associated_prescription_reference_number: Optional[str] = None
    associated_prescription_date: Optional[str] = None

class ClaimResponse(BaseModel):
    def __init__(self, *args, **kwargs):
        kwargs = {k: (None if v == "" else v) for k, v in kwargs.items()}
        super(ClaimResponse, self).__init__(*args, **kwargs)

    version: Optional[str] = None
    url: Optional[str] = None
    transaction_response_status: Optional[str] = None
    transaction_count: Optional[str] = None
    transaction_code: Optional[str] = None
    total_amount_paid: Optional[str] = None
    tax_exempt_indicator: Optional[str] = None
    service_provider_id_qualifier: Optional[str] = None
    service_provider_id: Optional[str] = None
    response_status: Optional[str] = None
    reject_field_occurrence_indicator: Optional[str] = None
    reject_count: Optional[str] = None
    reject_code: Optional[str] = None
    product_incentive: Optional[str] = None
    product_id_qualifier: Optional[str] = None
    product_id: Optional[str] = None
    product_description: Optional[str] = None
    product_count: Optional[str] = None
    product_cost_share_incentive: Optional[str] = None
    prescription_reference_number_qualifier: Optional[str] = None
    prescription_reference_number: Optional[str] = None
    plan_id: Optional[str] = None
    payer_id_qualifier: Optional[str] = None
    payer_id: Optional[str] = None
    patient_sales_tax_amount: Optional[str] = None
    patient_pay_amount: Optional[str] = None
    other_amount_paid_qualifier: Optional[str] = None
    other_amount_paid_count: Optional[str] = None
    other_amount_paid: Optional[str] = None
    network_reimbursement_id: Optional[str] = None
    message: Optional[str] = None
    ingredient_cost_paid: Optional[str] = None
    help_desk_phone_number_qualifier: Optional[str] = None
    help_desk_phone_number: Optional[str] = None
    group_id: Optional[str] = None
    flat_sales_tax_amount_paid: Optional[float] = None
    dispensing_fee_paid: Optional[str] = None
    date_of_service: Optional[str] = None
    date_of_birth: Optional[str] = None
    cardholder_id: Optional[str] = None
    basis_of_reimbursement_determination: Optional[str] = None
    authorization_number: Optional[str] = None
    amount_of_copay: Optional[str] = None
    amount_attributed_to_sales_tax: Optional[str] = None
    additional_message_information_qualifier: Optional[str] = None
    additional_message_information_count: Optional[str] = None
    additional_message_information_continuity: Optional[str] = None
    additional_message_information: Optional[str] = None


class ClaimTransferRequest(BaseModel):
    def __init__(self, *args, **kwargs):
        kwargs = {k: (None if v == "" else v) for k, v in kwargs.items()}
        super(ClaimTransferRequest, self).__init__(*args, **kwargs)

    processor_control_number: Optional[str] = None
    bin_number: Optional[str] = None


class ClaimTransferResponse(BaseModel):
    def __init__(self, *args, **kwargs):
        kwargs = {k: (None if v == "" else v) for k, v in kwargs.items()}
        super(ClaimTransferResponse, self).__init__(*args, **kwargs)

    version: Optional[str] = None
    transaction_response_status: Union[str, List[str]] = None
    transaction_count: Optional[str] = None
    transaction_code: Optional[str] = None
    service_provider_id_qualifier: Optional[str] = None
    service_provider_id: Optional[str] = None
    reject_count: Optional[str] = None
    reject_code: Union[str, List[str]] = None
    prescription_ref_num: Optional[str] = None
    prescription_number_qualifier: Optional[str] = None
    message: Optional[str] = None
    date_of_service: Optional[str] = None
    authorization_number: Optional[str] = None
    additional_message_information: Union[str, List[str]] = None


class Claim(BaseModel):
    def __init__(self, *args, **kwargs):
        kwargs = {k: (None if v == "" else v) for k, v in kwargs.items()}
        super(Claim, self).__init__(*args, **kwargs)

    claim_status: Optional[str] = None
    claim_request: Optional[ClaimRequest] = None
    claim_response: Optional[ClaimResponse] = None
    claim_transfer_request: Optional[ClaimTransferRequest] = None
    claim_transfer_response: Optional[ClaimTransferResponse] = None
    updateDate: Optional[str] = None
    type: str = 'claim'
    transactionId: Optional[str] = None
    startDate: Optional[str] = None
    sequenceNumber: Optional[str] = None
    prescription_id: Optional[str] = None
    overridenumber: Optional[str] = None
    override_thru: Optional[str] = None
    override_percentage: Optional[str] = None
    override_from: Optional[str] = None
    override_amount: Optional[str] = None
    over_ride: Optional[str] = None
    endDate: Optional[str] = None
    createDate: Optional[str] = None
    copay_override: Optional[str] = None
    autoerx_failure_reason: Optional[str] = None
    payer_dispensing_fee: Optional[float] = None
    auth_id: Optional[str] = None
    domain: Optional[str] = None
    mail_retail_code: Optional[str] = None
    brand_generic: Optional[str] = None
    baseline_cost: Optional[str] = None
    payer_ing_cost: Optional[float] = None
    tpa_member_id: Optional[str] = None
    drug_name: Optional[str] = None
    pharmacy_type: Optional[str] = None
    drug_dosage: Optional[str] = None
    awp_unit_price: Optional[str] = None
    drug_penalty: Optional[str] = None
    oop_accumulator_amount: Optional[str] = None
    gppc: Optional[str] = None
    drug_strength: Optional[str] = None
    drug_manufacturer: Optional[str] = None
    package_quantity: Optional[str] = None
    package_size: Optional[str] = None
    copay: Optional[str] = None
    copay_amt: Optional[str] = None
    copay_type: Optional[str] = None
    employee_opc: Optional[str] = None
    opc_remaining: Optional[str] = None
    price_type: Optional[str] = None
    pharmacy_name: Optional[str] = None
    pharmacy_chain_code: Optional[str] = None
    pharmacy_dispensing_fee: Optional[str] = None
    default_payment_option: Optional[str] = None
    claims_processor: Optional[str] = None
    payer_patient_paid_amount: Optional[float] = None
    plan_year: Optional[str] = None
    deductible_accumulator_amount: Optional[str] = None
    coverage_tier_name: Optional[str] = None
    benefit_plan_name: Optional[str] = None
    alternative_drug_rewards: Optional[str] = None
    total_reward: Optional[str] = None
    rebate_factor: Optional[str] = None
    manufacturer_name: Optional[str] = None
    rebate_amount: Optional[str] = None
    retail_reward: Optional[str] = None
    awp_amount: Optional[str] = None
    stocking_fee: Optional[str] = None
    admin_fee: Optional[str] = None
    reward_percentage: Optional[str] = None
    reward_share: Optional[str] = None
    rewards: Optional[str] = None
    payer_sales_tax: Optional[float] = None
    otc_indicator: Optional[str] = None
    multi_source: Optional[str] = None
    pa_flag: Optional[str] = None
    payer_authid: Optional[str] = None
    payee_type: Optional[str] = None
    submitted_total_amount: Optional[str] = None
    alternate_penalty: Optional[str] = None
    client_deductible: Optional[str] = None
    calculated_disp_fee: Optional[str] = None
    calculated_drug_cost: Optional[str] = None
    calculated_employee_opc: Optional[str] = None
    calculated_employer_cost: Optional[str] = None
    calculated_ing_cost: Optional[str] = None
    calculated_patient_pay_amt: Optional[str] = None
    client_disp_fee_paid: Optional[str] = None
    client_drug_cost_paid: Optional[str] = None
    client_employee_paid: Optional[str] = None
    client_employer_cost: Optional[str] = None
    client_ing_cost: Optional[str] = None
    submitted_disp_fee: Optional[str] = None
    submitted_drug_cost: Optional[str] = None
    submitted_employer_cost: Optional[str] = None
    submitted_ing_cost: Optional[str] = None
    submitted_patient_paid_amount: Optional[str] = None
    unc_disp_fee: Optional[str] = None
    unc_drug_cost: Optional[str] = None
    member_group: Optional[str] = None
    unc_employer_cost: Optional[str] = None
    unc_ing_cost: Optional[str] = None
    unc_patient_paid_amount: Optional[str] = None
    unit_price: Optional[str] = None
    unit_price_before_rebate: Optional[float] = None
    payer_client_due_amt: Optional[float] = None
    rx_flipt_person_id: Optional[str] = None
    employee_id: Optional[str] = None
    specialty_flag: Optional[str] = None
    member_choice_penalty_amount: Optional[str] = None
    payer_sequence_number: Optional[str] = None
    erx_status: Optional[str] = None
    client_patient_sales_tax_amount_paid: Optional[str] = None
    client_plan_sales_tax_amount_paid: Optional[str] = None
    deductible_accumulator_flag: Optional[Literal['Y', 'N']] = None
    oop_accumulator_flag: Optional[Literal['Y', 'N']]
    incentive_credit_applied: Optional[str] = None
    incentive_credit_remaining: Optional[str] = None
    process_error_code: Optional[str] = None
    rds_subsidy_determination_indicator: Optional[str] = None
    medicare_type: Optional[str] = None
