import {instance} from "../config/api"

export const login = async (email: string, password: string) => {
  try {
    const response = await instance.post('auth/login', {
      email,
      password
    })
    return response.data
  } catch (error) {
    return false
  }
}

export const sales_month = async (access_token:string) => {
  try {
    const response = await instance.post("manager/sales-month",{
      store_id:"MG_21"
    },{headers:{Authorization:`Bearer ${access_token}`}})

    return response.data
  } catch (error) {
    return false
  }
}

export const performance_by_store_six = async(access_token:string) => {
  try {
    const response = await instance.post("manager/performance-by-store-six",{
      store_id:"MG_21"
    },{headers:{Authorization:`Bearer ${access_token}`}})

    return response.data
  } catch (error) {
    return false
  }
}

export const top_product = async(access_token:string) => {
  try {
    const response = await instance.post("manager/top-products",{
      store_id:"MG_21"
    },{headers:{Authorization:`Bearer ${access_token}`}})

    console.log(response.data)
    return response.data
  } catch (error) {
    return false
  }
}

export const top_category = async(access_token:string) => {
  try {
    const response = await instance.post("manager/top-categories",{
      store_id:"MG_21"
    },{headers:{Authorization:`Bearer ${access_token}`}})

    console.log(response.data)
    return response.data
  } catch (error) {
    return false
  }
}

export const sellers_performance = async(access_token:string) => {
  try {
    const response = await instance.post("manager/sellers-performance",{
      store_id:"MG_21"
    },{headers:{Authorization:`Bearer ${access_token}`}})

    console.log(response.data)
    return response.data
  } catch (error) {
    return false
  }
}

export const salesMan_target = async(access_token:string) => {
  try {
    const response = await instance.post("sales-man/sales-target",{
      user_id:"567"
   },{headers:{Authorization:`Bearer ${access_token}`}})
 
   return response.data
  } catch (error) {
    return false
  }
}

export const salesMan_inventory = async(access_token:string) => {
  try {
    const response = await instance.post("sales-man/inventory",{
      store_id:"MG_21"
   },{headers:{Authorization:`Bearer ${access_token}`}})
 
   return response.data
  } catch (error) {
    return false
  }
}

export const salesMan_recomendation = async(access_token:string,product_id:string) => {
  try {
    const response = await instance.post("sales-man/recomendation",{
      product_id:product_id
   },{headers:{Authorization:`Bearer ${access_token}`}})
 
   return response.data
  } catch (error) {
    return false
  }
}