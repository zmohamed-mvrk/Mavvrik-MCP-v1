from typing import List, Optional, Any, Dict, Literal
from pydantic import BaseModel, Field, ConfigDict

# --- Primitives & Scalars ---
Json = Dict[str, Any]

class iTag(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None

class Search(BaseModel):
    fields: Optional[List[str]] = None
    keyword: Optional[str] = None

class iSPPlannerSP(BaseModel):
    id: Optional[str] = None
    scope: Optional[str] = None
    account: Optional[str] = None
    billing_account_id: Optional[str] = None
    hourly_commitment: Optional[float] = None
    term: Optional[str] = None
    instance_family: Optional[str] = None
    location_id: Optional[str] = None
    payment_option: Optional[str] = None
    type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

# --- Main Filter Input ---
class Filter(BaseModel):
    """
    Comprehensive Filter input.
    'json' field is aliased to 'json_value' to avoid Pydantic conflicts.
    """
    model_config = ConfigDict(populate_by_name=True)

    provider_code: Optional[List[str]] = None
    product_name: Optional[List[str]] = None
    asset_type: Optional[List[str]] = None
    billing_account_id: Optional[List[str]] = None
    usage_account_id: Optional[List[str]] = None
    billing_account_name: Optional[List[str]] = None
    usage_account_name: Optional[List[str]] = None
    location_id: Optional[List[str]] = None
    location_name: Optional[List[str]] = None
    tag_keys: Optional[List[str]] = None
    vtag_keys: Optional[List[str]] = None
    tags: Optional[List[iTag]] = None
    vtags: Optional[List[iTag]] = None
    category: Optional[List[str]] = None
    severity: Optional[List[str]] = None
    type: Optional[List[str]] = None
    policy_id: Optional[List[str]] = None
    state: Optional[List[str]] = None
    term: Optional[List[str]] = None
    instance_type: Optional[List[str]] = None
    purchase_option: Optional[List[str]] = None
    platform: Optional[List[str]] = None
    cluster: Optional[List[str]] = None
    namespace: Optional[List[str]] = None
    node_pool: Optional[List[str]] = None
    node: Optional[List[str]] = None
    pv: Optional[List[str]] = None
    pv_storage_class: Optional[List[str]] = None
    pvc: Optional[List[str]] = None
    gpu_model: Optional[List[str]] = None
    gpu_gi_profile: Optional[List[str]] = None
    controller_kind: Optional[List[str]] = None
    cost_type: Optional[List[str]] = None
    payment_option: Optional[List[str]] = None
    instance_family: Optional[List[str]] = None
    cloud_resource_id: Optional[List[str]] = None
    deployment_option: Optional[List[str]] = None
    reservations: Optional[List[str]] = None
    savings_plans: Optional[List[str]] = None
    resource_type: Optional[List[str]] = None
    resource_category: Optional[List[str]] = None
    vcenter_id: Optional[List[str]] = None
    datacenter_id: Optional[List[str]] = None
    cluster_id: Optional[List[str]] = None
    host_id: Optional[List[str]] = None
    vcenter_name: Optional[List[str]] = None
    datacenter_name: Optional[List[str]] = None
    cluster_name: Optional[List[str]] = None
    host_name: Optional[List[str]] = None
    resource_id: Optional[List[str]] = None
    resource_name: Optional[List[str]] = None
    reservation_id: Optional[List[str]] = None
    savings_plan_id: Optional[List[str]] = None
    host_vendor: Optional[List[str]] = None
    host_model: Optional[List[str]] = None
    tenancy: Optional[List[str]] = None
    cost_category: Optional[List[str]] = None
    resource_group_id: Optional[List[str]] = None
    customer_id: Optional[List[str]] = None
    customer_name: Optional[List[str]] = None
    sku_id: Optional[List[str]] = None
    sku_name: Optional[List[str]] = None
    billing_entity: Optional[List[str]] = None
    
    # FIX: Renamed field to avoid shadow warning
    json_value: Optional[Json] = Field(None, alias="json")
    
    tenant_id: Optional[List[str]] = None
    tenant_name: Optional[List[str]] = None
    usage_type: Optional[List[str]] = None
    model: Optional[List[str]] = None
    model_provider_code: Optional[List[str]] = None
    model_type: Optional[List[str]] = None
    model_family: Optional[List[str]] = None
    model_service: Optional[List[str]] = None
    model_name: Optional[List[str]] = None
    model_version: Optional[List[str]] = None
    operation: Optional[List[str]] = None
    source: Optional[List[str]] = None

class AlertFilter(BaseModel):
    """Filter specifically for AlertOption"""
    model_config = ConfigDict(populate_by_name=True)
    
    type: Optional[List[str]] = None
    users: Optional[List[str]] = None
    channels: Optional[List[str]] = None
    
    # FIX: Renamed field to avoid shadow warning
    json_value: Optional[Json] = Field(None, alias="json")

# --- Query Options ---

class CostOption(BaseModel):
    interval: Optional[str] = None
    variance: Optional[str] = None
    groupBy: Optional[str] = None
    fromDate: Optional[str] = Field(None, description="Format: YYYY-MM-01 or YYYY-MM-DD")
    toDate: Optional[str] = Field(None, description="Format: YYYY-MM-01 or YYYY-MM-DD")
    todayDate: Optional[str] = None
    tagKey: Optional[str] = None
    tagKeys: Optional[List[str]] = None
    vtagKey: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    limit: Optional[int] = None
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    chartType: Optional[str] = None
    forecast: Optional[int] = None
    category: Optional[str] = None
    month: Optional[str] = None
    options: Optional[List[str]] = None
    optionsMap: Optional[Json] = None
    costFieldsMap: Optional[Json] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    filterKey: Optional[str] = None
    mode: Optional[str] = None
    costAllocationId: Optional[str] = None
    costToServeId: Optional[str] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None
    provider: Optional[str] = None
    fieldIds: Optional[List[str]] = None

class CompareUnitCostOption(BaseModel):
    interval: Optional[str] = None
    xAxis: Optional[str] = None
    chartType: Optional[str] = None
    groupBy: Optional[str] = None
    limit: Optional[int] = None
    category: Optional[str] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    month: Optional[str] = None
    todayDate: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None

class AssetOption(BaseModel):
    groupBy: Optional[str] = None
    tagKey: Optional[str] = None
    vtagKey: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    todayDate: Optional[str] = None
    limit: Optional[int] = None
    category: Optional[str] = None
    month: Optional[str] = None
    i18nMap: Optional[Json] = None

class ResourceOption(BaseModel):
    interval: Optional[str] = None
    yAxis: Optional[str] = None
    xAxis: Optional[str] = None
    groupBy: Optional[str] = None
    tagKey: Optional[str] = None
    vtagKey: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    todayDate: Optional[str] = None
    limit: Optional[int] = None
    category: Optional[str] = None
    month: Optional[str] = None
    options: Optional[List[str]] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None

class TagOption(BaseModel):
    interval: Optional[str] = None
    groupBy: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    limit: Optional[int] = None
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    chartType: Optional[str] = None
    month: Optional[str] = None
    todayDate: Optional[str] = None
    options: Optional[List[str]] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    i18nMap: Optional[Json] = None
    vtagKey: Optional[str] = None
    tagKeys: Optional[List[str]] = None
    dateRanges: Optional[List[List[str]]] = None
    tagPolicy: Optional[Filter] = None

class DCUtilizationOption(BaseModel):
    interval: Optional[str] = None
    month: Optional[str] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    todayDate: Optional[str] = None
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    chartType: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    category: Optional[str] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None

class K8sUtilizationOption(BaseModel):
    interval: Optional[str] = None
    month: Optional[str] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    todayDate: Optional[str] = None
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    chartType: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    category: Optional[str] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None

class RecommendationOption(BaseModel):
    todayDate: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    i18nMap: Optional[Json] = None
    options: Optional[List[str]] = None
    thresholds: Optional[Json] = None

class CoverageOption(BaseModel):
    interval: Optional[str] = None
    date: Optional[str] = None
    month: Optional[str] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    todayDate: Optional[str] = None
    chartType: Optional[str] = None
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None

class RIOption(BaseModel):
    interval: Optional[str] = None
    date: Optional[str] = None
    month: Optional[str] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    todayDate: Optional[str] = None
    chartType: Optional[str] = None
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None

class SPOption(BaseModel):
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    date: Optional[str] = None
    month: Optional[str] = None
    todayDate: Optional[str] = None
    chartType: Optional[str] = None
    xAxis: Optional[str] = None
    yAxis: Optional[str] = None
    interval: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    i18nMap: Optional[Json] = None
    dateRanges: Optional[List[List[str]]] = None

class AnomalyOption(BaseModel):
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    month: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    limit: Optional[int] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    i18nMap: Optional[Json] = None
    level: Optional[int] = None
    thresholds: Optional[Json] = None

class AgentSessionOption(BaseModel):
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    month: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    limit: Optional[int] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    i18nMap: Optional[Json] = None
    sessionId: Optional[str] = None

class SPPlannerOption(BaseModel):
    todayDate: Optional[str] = None
    month: Optional[str] = None
    provider: Optional[str] = None
    currency: Optional[str] = None
    savingsPlans: Optional[List[iSPPlannerSP]] = None

class CostAllocationOption(BaseModel):
    id: Optional[str] = None
    month: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    i18nMap: Optional[Json] = None

class AlertOption(BaseModel):
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None
    i18nMap: Optional[Json] = None

class ReportOption(BaseModel):
    pageNo: Optional[int] = None
    pageSize: Optional[int] = None

# --- Helper Payload Wrapper ---
class GraphQLPayload(BaseModel):
    option: Optional[CostOption] = None
    filter: Optional[Filter] = None
    search: Optional[Search] = None