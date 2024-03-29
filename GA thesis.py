#%%
# Filter FutureWarning messages
import warnings
import pandas as pd
import numpy as np
import random
import math
import os
import datetime
from random import choice
from more_itertools import locate
from collections import OrderedDict
from math import sqrt
import time
import logging
import matplotlib.pyplot as plt
import sys
import copy
import csv
import win32api
from knockknock import email_sender
warnings.simplefilter(action="ignore", category=FutureWarning)


    
#%%
# read data from input file and return parameters/variables
def read_data(df_VM_info, input_excel, input_sheet_ProEast, input_sheet_ProNotEast, input_sheet_ProDemand, Index_strart, Index_end):  
    
    # Input data from (VM_info.sheet)
    # CargoLane_TotalNumber = int(df_VM_info.at[Index_strart, "CargoLane_TotalNumber"])
    # CargoLane_TotalNumber = int(len((df_VM_info["CargoLane_ID"].squeeze()).tolist()) -1) # 直接抓最大的ID
    CargoLane_TotalNumber = int((df_VM_info["CargoLane_TotalNumber"].squeeze()).tolist()[0])
    VM_ID = df_VM_info.at[Index_strart, "VM_ID"]
    CargoLane_Device_ID = (df_VM_info.loc[Index_strart:Index_end, ["Device_ID"]].squeeze()).tolist()
    CargoLane_Site_ID = (df_VM_info.loc[Index_strart:Index_end, ["Site_ID"]].squeeze()).tolist()
    CargoLane_ID = (df_VM_info.loc[Index_strart:Index_end, ["CargoLane_ID"]].squeeze()).tolist()
    CargoLane_Type = (df_VM_info.loc[Index_strart:Index_end, ["CargoLane_Type"]].squeeze()).tolist()
    CargoLane_Height_Max = (df_VM_info.loc[Index_strart:Index_end, ["High_Max"]].squeeze()).tolist()
    CargoLane_Height_Min = (df_VM_info.loc[Index_strart:Index_end, ["High_Min"]].squeeze()).tolist()
    CargoLane_Diameter_Max_1 = (df_VM_info.loc[Index_strart:Index_end, ["Diameter_Max_1"]].squeeze()).tolist()
    CargoLane_Diameter_Min_1 = (df_VM_info.loc[Index_strart:Index_end, ["Diameter_Min_1"]].squeeze()).tolist()
    CargoLane_Area = (df_VM_info.loc[Index_strart:Index_end, ["Area"]].squeeze()).tolist()
    CargoLane_Capacity = (df_VM_info.loc[Index_strart:Index_end, ["CargoLane_Capacity"]].squeeze()).tolist()
    Current_Product = (df_VM_info.loc[Index_strart:Index_end, ["Current_Product"]].squeeze()).tolist()
    Max_Prod_Cnt = df_VM_info.at[Index_strart, "Max_Prod_Cnt"]
    Min_Prod_Cnt = df_VM_info.at[Index_strart, "Min_Prod_Cnt"]
    CargoLane_Allow_Special = (df_VM_info.loc[Index_strart:Index_end, ["Allow_Special"]].squeeze()).tolist()
    CargoLane_Average_Replenishment = (df_VM_info.loc[Index_strart:Index_end, ["Average_Replenishment"]].squeeze()).tolist()
    CargoLane_Category_Rate = (df_VM_info.loc[Index_strart:Index_end, ["Category_Rate"]].squeeze()).tolist()
    CargoLane_Brand_Rate = (df_VM_info.loc[Index_strart:Index_end, ["Brand_Rate"]].squeeze()).tolist()
    
    # distinguish the cargolane type which can allow special size from normal(can not allow)
    for i in range(len(CargoLane_Type)):
        if CargoLane_Type[i] == 5:
            pass
        elif CargoLane_Allow_Special[i] == 1:
            CargoLane_Type[i] = "s" + str(CargoLane_Type[i])
            
        CargoLane_ID[i] = int(CargoLane_ID[i]) # !!!!!
    
    df_Product_info = pd.read_excel(input_excel, sheet_name = "Product_info")
    
    # Input data from (Product_info.sheet)
    Product_ID = df_Product_info["Product_ID"].tolist()
    Product_Price = df_Product_info["Price"].tolist()
    Product_Cost = df_Product_info["Cost"].tolist()
    Product_Product_sales = df_Product_info["Average_sales_month"].tolist()
    Product_Type = df_Product_info["Type"].tolist()
    Product_Volume = df_Product_info["Volume"].tolist()
    Product_Length = df_Product_info["length"].tolist()
    Product_Width = df_Product_info["width"].tolist()
    Product_Height = df_Product_info["height"].tolist()
    Product_New = df_Product_info["New"].tolist()
    Product_Brand = df_Product_info["Brand"].tolist()
    Product_Category = df_Product_info["Category"].tolist()
    Product_Specialsize = df_Product_info["Special_size"].tolist()
    #Product_Operating_cost = df_Product_info["Operating_cost"].tolist()
    #Product_Total_produced = df_Product_info["Total_produced"].tolist()
    
    unit_purc_cost=[]
    
    # random.seed(0)
    # for i in range(len( Product_ID)):
        # rand_purch = random.uniform(10, 20)
        #rand_pr= random.uniform(20, 40)
        # unit_purc_cost.append(rand_purch)
        #pr_price.append(rand_pr)
    # Product_Cost= unit_purc_cost
   
    df_Product_demand = pd.read_excel(input_excel, sheet_name = input_sheet_ProDemand)
    
    # Input data from (Product_demand.sheet)
    Demand_Product_ID = df_Product_demand["Product_ID"].tolist()
    Demand_Product_Sales = df_Product_demand["Average_sales_month"].tolist()
    
    # variable for saving ID which Demand_sales = 0
    Demand_zero = []
    for i in range(len(Demand_Product_Sales)):
        if Demand_Product_Sales[i] == 0:
            Demand_zero.append(Demand_Product_ID[i])
    
    # Input data from (Product_Repel.sheet)
    df_replacement_matrix = pd.read_excel(input_excel, sheet_name = "Product_Repel")
    df_replacement_matrix.set_index("Unnamed: 0", inplace=True)
    
    replacement_index = df_replacement_matrix.index
    replacement_matrix = {}
    for i in range(len(replacement_index)):
        # print(replacement_index[i])
        # print(df_replacement_matrix[replacement_index[i]].loc[df_replacement_matrix[replacement_index[i]]==1].keys().tolist()[0])
        replacement_matrix.setdefault(replacement_index[i], df_replacement_matrix[replacement_index[i]].loc[df_replacement_matrix[replacement_index[i]]==1].keys().tolist()[0])
     
    # 0913
    for i in range(len(Product_New)):
         if Product_New[i] == 1 and Product_ID[i] in Demand_Product_ID:
             Product_New[i] = 0
             
    return df_VM_info, df_Product_info, df_Product_demand, df_replacement_matrix, VM_ID, CargoLane_Device_ID, CargoLane_Site_ID, CargoLane_TotalNumber, CargoLane_ID, CargoLane_Type, \
        CargoLane_Height_Max, CargoLane_Height_Min, CargoLane_Diameter_Max_1, CargoLane_Diameter_Min_1, \
        CargoLane_Area, CargoLane_Capacity, Current_Product, Max_Prod_Cnt, Min_Prod_Cnt, CargoLane_Allow_Special, \
        CargoLane_Average_Replenishment, CargoLane_Category_Rate, CargoLane_Brand_Rate, \
        Product_ID, Product_Price, Product_Cost, Product_Product_sales, Product_Type, Product_Volume, Product_Length, Product_Width, Product_Height, Product_New, \
        Product_Brand, Product_Category, Product_Specialsize, Demand_Product_ID, Demand_Product_Sales, replacement_matrix, Demand_zero

#%%
# declare variables to save info(like ID, price, sales, cost etc)
def classify_demand_product(Product_ID, Product_Type, Product_Volume, Product_Price, Demand_Product_ID, Demand_Product_Sales, CargoLane_Average_Replenishment, Product_New, Product_Brand, Product_Specialsize, Product_Cost):
    # ID, price, cost, sales variables for different type
    ID_CargoLane1 = []
    ID_CargoLane2 = []
    ID_CargoLane3 = []
    ID_CargoLane4 = []
    ID_CargoLane5 = []
    
    Price_CargoLane1 = []    
    Price_CargoLane2 = []    
    Price_CargoLane3 = []    
    Price_CargoLane4 = []    
    Price_CargoLane5 = []

    Cost_CargoLane1 = []
    Cost_CargoLane2 = []
    Cost_CargoLane3 = []
    Cost_CargoLane4 = []
    Cost_CargoLane5 = []

    Sales_CargoLane1 = []    
    Sales_CargoLane2 = []    
    Sales_CargoLane3 = []    
    Sales_CargoLane4 = []    
    Sales_CargoLane5 = []
    
    # s: only special
    sID_CargoLane1 = []
    sID_CargoLane2 = []
    sID_CargoLane3 = []
    sID_CargoLane4 = []
    
    sPrice_CargoLane1 = []    
    sPrice_CargoLane2 = []    
    sPrice_CargoLane3 = []    
    sPrice_CargoLane4 = []    

    sCost_CargoLane1 = []
    sCost_CargoLane2 = []
    sCost_CargoLane3 = []
    sCost_CargoLane4 = []

    sSales_CargoLane1 = []    
    sSales_CargoLane2 = []    
    sSales_CargoLane3 = []    
    sSales_CargoLane4 = []    
    

    
    # sn: special and normal
    snID_CargoLane1 = []
    snID_CargoLane2 = []
    snID_CargoLane3 = []
    snID_CargoLane4 = []
    
    snPrice_CargoLane1 = []    
    snPrice_CargoLane2 = []    
    snPrice_CargoLane3 = []    
    snPrice_CargoLane4 = []    

    snCost_CargoLane1 = []
    snCost_CargoLane2 = []
    snCost_CargoLane3 = []
    snCost_CargoLane4 = []

    snSales_CargoLane1 = []    
    snSales_CargoLane2 = []    
    snSales_CargoLane3 = []    
    snSales_CargoLane4 = []    
    

    New_ID1 = []
    New_ID2 = []
    New_ID3 = []
    New_ID4 = []
    New_ID5 = []
    
    New_profit1 = []
    New_profit2 = []
    New_profit3 = []
    New_profit4 = []
    New_profit5 = []
    
    Brand_CargoLane1 = []
    Brand_CargoLane2 = []
    Brand_CargoLane3 = []
    Brand_CargoLane4 = []
    Brand_CargoLane5 = []
    
    # s: only special
    sNew_ID1 = []
    sNew_ID2 = []
    sNew_ID3 = []
    sNew_ID4 = []
    
    sNew_profit1 = []
    sNew_profit2 = []
    sNew_profit3 = []
    sNew_profit4 = []
    
    sBrand_CargoLane1 = []
    sBrand_CargoLane2 = []
    sBrand_CargoLane3 = []
    sBrand_CargoLane4 = []
    
    # sn: special and normal
    snNew_ID1 = []
    snNew_ID2 = []
    snNew_ID3 = []
    snNew_ID4 = []
    
    snNew_profit1 = []
    snNew_profit2 = []
    snNew_profit3 = []
    snNew_profit4 = []
    
    snBrand_CargoLane1 = []
    snBrand_CargoLane2 = []
    snBrand_CargoLane3 = []
    snBrand_CargoLane4 = []
    
    unit_inventory_cost=[]
    unit_backroom_cost=[]
    unit_display_cost=[]
    unit_ordering_cost=[]
    
    
    # calculate info about replenishment
    replenishment_per_time = []                                                # demand/replenishment lead time
    Cargolanetype_sum_capacity = [0] * 6                                       # sum of the capacity with same cargolane type 
    # print(Cargolanetype_sum_capacity)
    Cargolanetype_average_capacity = [0] * 6                                   # average of the capacity with same cargolane type
    demand_product_typenum = [6] * len(Demand_Product_ID)                      # Product Demand product type
    # print(demand_product_typenum)
    product_product_typenum = [6] * len(Product_ID)                            # Product_info product type
    Product_max_cargolanenum = []
    cargolane_should_empty = []
    
    #generate cost data for unit product
    
    #Inventory Cost
    random.seed(0)
    for i in range(len(Product_ID)):
        rand_inv = random.uniform(2.0, 4.0)
        rand_backroom= random.uniform(1.0, 2.0)
        rand_display= random.uniform(1.0, 3.0)
        unit_inventory_cost.append(rand_inv)
        unit_backroom_cost.append(rand_backroom)
        unit_display_cost.append(rand_display)
    
    for i in Product_Price:
        unit_ordering_cost.append(50) 

    count= CargoLane_Capacity.count(0)
    count_cap= len(CargoLane_Capacity) - count
    
    setup= 0
    replenishment_time= 4
    rep_fee= 0
    replenishment= rep_fee * replenishment_time
    
    setup_cost= setup/count_cap
    replenishment_cost= replenishment/count_cap
    
    # saving info to corresponding list
    for i in range(0, len(Demand_Product_ID), 1):
        replenishment_per_time.append((Demand_Product_Sales[i] / (30 / (CargoLane_Average_Replenishment[0] ))))
        for j in range(0, len(Product_ID), 1):
            if Demand_Product_ID[i] == Product_ID[j]:
                
                if Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0:
                    ID_CargoLane1.append(Demand_Product_ID[i])
                    Price_CargoLane1.append(Product_Price[j])
                    Cost_CargoLane1.append(Product_Cost[j])
                    Sales_CargoLane1.append(Demand_Product_Sales[i])
                    Brand_CargoLane1.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     New_ID1.append(Product_ID[j])
                    #     New_profit1.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if product_product_typenum[j] > 1:
                        product_product_typenum[j] = 1
                if Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1:
                    sID_CargoLane1.append(Demand_Product_ID[i])
                    sPrice_CargoLane1.append(Product_Price[j])
                    sCost_CargoLane1.append(Product_Cost[j])
                    sSales_CargoLane1.append(Demand_Product_Sales[i])
                    sBrand_CargoLane1.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     sNew_ID1.append(Product_ID[j])
                    #     sNew_profit1.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if type(product_product_typenum[j]) == int:
                        if product_product_typenum[j] > 1:
                            product_product_typenum[j] = "s1.0"
                    elif type(product_product_typenum[j]) == str:
                        if int(product_product_typenum[j][1]) > 1:
                            product_product_typenum[j] = "s1.0"
                if Product_Type[j] == "CAN" and Product_Volume[j] <= 330:
                    snID_CargoLane1.append(Demand_Product_ID[i])
                    snPrice_CargoLane1.append(Product_Price[j])
                    snCost_CargoLane1.append(Product_Cost[j])
                    snSales_CargoLane1.append(Demand_Product_Sales[i])
                    snBrand_CargoLane1.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     snNew_ID1.append(Product_ID[j])
                    #     snNew_profit1.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if demand_product_typenum[i] > 1:
                        demand_product_typenum[i] = 1
                    # if product_product_typenum[j] > 1:
                    #     product_product_typenum[j] = 1
                    
                if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0)\
                    or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0):
                    ID_CargoLane2.append(Demand_Product_ID[i])
                    Price_CargoLane2.append(Product_Price[j])
                    Cost_CargoLane2.append(Product_Cost[j])
                    Sales_CargoLane2.append(Demand_Product_Sales[i])
                    Brand_CargoLane2.append(Product_Brand[j])
                    # print(Price_CargoLane2)
                    # if Product_New[j] == 1:
                    #     New_ID2.append(Product_ID[j])
                    #     New_profit2.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if product_product_typenum[j] > 2:
                        product_product_typenum[j] = 2
                if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1)\
                    or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1):            #gaada
                    sID_CargoLane2.append(Demand_Product_ID[i])
                    sPrice_CargoLane2.append(Product_Price[j])
                    sCost_CargoLane2.append(Product_Cost[j])
                    sSales_CargoLane2.append(Demand_Product_Sales[i])
                    sBrand_CargoLane2.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     sNew_ID2.append(Product_ID[j])
                    #     sNew_profit2.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if type(product_product_typenum[j]) == int:
                        if product_product_typenum[j] > 2:
                            product_product_typenum[j] = "s2.0"
                    elif type(product_product_typenum[j]) == str:
                        if int(product_product_typenum[j][1]) > 2:
                            product_product_typenum[j] = "s2.0"
                if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330)\
                    or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330):
                    snID_CargoLane2.append(Demand_Product_ID[i])
                    snPrice_CargoLane2.append(Product_Price[j])
                    snCost_CargoLane2.append(Product_Cost[j])
                    snSales_CargoLane2.append(Demand_Product_Sales[i])
                    snBrand_CargoLane2.append(Product_Brand[j])
                    
                    # if Product_New[j] == 1:
                    #     snNew_ID2.append(Product_ID[j])
                    #     snNew_profit2.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if demand_product_typenum[i] > 2:
                        demand_product_typenum[i] = 2
                    # if product_product_typenum[j] > 2:
                    #     product_product_typenum[j] = 2
                    
                if (Product_Type[j] == "PET" and Product_Volume[j] <= 500 and Product_Specialsize[j] == 0):
                    ID_CargoLane3.append(Demand_Product_ID[i])
                    Price_CargoLane3.append(Product_Price[j])
                    Cost_CargoLane3.append(Product_Cost[j])
                    Sales_CargoLane3.append(Demand_Product_Sales[i])
                    Brand_CargoLane3.append(Product_Brand[j])
                    # print(Price_CargoLane3)
                    # if Product_New[j] == 1:
                    #     New_ID3.append(Product_ID[j])
                    #     New_profit3.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if product_product_typenum[j] > 3:
                        product_product_typenum[j] = 3
                if (Product_Type[j] == "PET" and Product_Volume[j] <= 500 and Product_Specialsize[j] == 1):
                    sID_CargoLane3.append(Demand_Product_ID[i])
                    sPrice_CargoLane3.append(Product_Price[j])
                    sCost_CargoLane3.append(Product_Cost[j])
                    sSales_CargoLane3.append(Demand_Product_Sales[i])
                    sBrand_CargoLane3.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     sNew_ID3.append(Product_ID[j])
                    #     sNew_profit3.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if type(product_product_typenum[j]) == int:
                        if product_product_typenum[j] > 3:
                            product_product_typenum[j] = "s3.0"
                    elif type(product_product_typenum[j]) == str:
                        if int(product_product_typenum[j][1]) > 3:
                            product_product_typenum[j] = "s3.0"
                if (Product_Type[j] == "PET" and Product_Volume[j] <= 500):
                    snID_CargoLane3.append(Demand_Product_ID[i])
                    snPrice_CargoLane3.append(Product_Price[j])
                    snCost_CargoLane3.append(Product_Cost[j])
                    snSales_CargoLane3.append(Demand_Product_Sales[i])
                    snBrand_CargoLane3.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     snNew_ID3.append(Product_ID[j])
                    #     snNew_profit3.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if demand_product_typenum[i] > 3:
                        demand_product_typenum[i] = 3
                    # if product_product_typenum[j] > 3:
                    #     product_product_typenum[j] = 3
                    
                if (Product_Type[j] == "PET" and Product_Volume[j] <= 600 and Product_Specialsize[j] == 0):
                    ID_CargoLane4.append(Demand_Product_ID[i])
                    Price_CargoLane4.append(Product_Price[j])
                    Cost_CargoLane4.append(Product_Cost[j])
                    Sales_CargoLane4.append(Demand_Product_Sales[i])
                    Brand_CargoLane4.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     New_ID4.append(Product_ID[j])
                    #     New_profit4.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if product_product_typenum[j] > 4:
                        product_product_typenum[j] = 4
                if (Product_Type[j] == "PET" and Product_Volume[j] <= 600 and Product_Specialsize[j] == 1):
                    sID_CargoLane4.append(Demand_Product_ID[i])
                    sPrice_CargoLane4.append(Product_Price[j])
                    sCost_CargoLane4.append(Product_Cost[j])
                    sSales_CargoLane4.append(Demand_Product_Sales[i])
                    sBrand_CargoLane4.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     sNew_ID4.append(Product_ID[j])
                    #     sNew_profit4.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if type(product_product_typenum[j]) == int:
                        if product_product_typenum[j] > 4:
                            product_product_typenum[j] = "s4.0"
                    elif type(product_product_typenum[j]) == str:
                        if int(product_product_typenum[j][1]) > 4:
                            product_product_typenum[j] = "s4.0"
                if (Product_Type[j] == "PET" and Product_Volume[j] <= 600):
                    snID_CargoLane4.append(Demand_Product_ID[i])
                    snPrice_CargoLane4.append(Product_Price[j])
                    snCost_CargoLane4.append(Product_Cost[j])
                    snSales_CargoLane4.append(Demand_Product_Sales[i])
                    snBrand_CargoLane4.append(Product_Brand[j])
                    # if Product_New[j] == 1:
                    #     snNew_ID4.append(Product_ID[j])
                    #     snNew_profit4.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if demand_product_typenum[i] > 4:
                        demand_product_typenum[i] = 4
                    # if product_product_typenum[j] > 4:
                    #     product_product_typenum[j] = 4
                    
                if Product_Type[j] == "PET" and Product_Volume[j] <= 600:
                    ID_CargoLane5.append(Demand_Product_ID[i])
                    Price_CargoLane5.append(Product_Price[j])
                    Cost_CargoLane5.append(Product_Cost[j])
                    Sales_CargoLane5.append(Demand_Product_Sales[i])
                    Brand_CargoLane5.append(Product_Brand[j])
                    # print(Price_CargoLane5z)
                    # if Product_New[j] == 1:
                    #     New_ID5.append(Product_ID[j])
                    #     New_profit5.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])
                    if demand_product_typenum[i] > 5:
                        demand_product_typenum[i] = 5
                        
    ##########################################################################
    for j in range(len(Product_ID)):
        if Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0:
            if Product_New[j] == 1:
                New_ID1.append(Product_ID[j])
                New_profit1.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) # - (setup_cost+replenishment_cost))
            if product_product_typenum[j] > 1:
                product_product_typenum[j] = 1
        if Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1:
            if Product_New[j] == 1:
                sNew_ID1.append(Product_ID[j])
                sNew_profit1.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) # -(setup_cost+replenishment_cost))
            if type(product_product_typenum[j]) == int:
                if product_product_typenum[j] > 1:
                    product_product_typenum[j] = "s1.0"
            elif type(product_product_typenum[j]) == str:
                if int(product_product_typenum[j][1]) > 1:
                    product_product_typenum[j] = "s1.0"
        if Product_Type[j] == "CAN" and Product_Volume[j] <= 330:
            if Product_New[j] == 1:
                snNew_ID1.append(Product_ID[j])
                snNew_profit1.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
                    
        if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0)\
            or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0):
            if Product_New[j] == 1:
                New_ID2.append(Product_ID[j])
                New_profit2.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
            if product_product_typenum[j] > 2:
                product_product_typenum[j] = 2
        if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1)\
            or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1):
            if Product_New[j] == 1:
                sNew_ID2.append(Product_ID[j])
                sNew_profit2.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
            if type(product_product_typenum[j]) == int:
                if product_product_typenum[j] > 2:
                    product_product_typenum[j] = "s2.0"
            elif type(product_product_typenum[j]) == str:
                if int(product_product_typenum[j][1]) > 2:
                    product_product_typenum[j] = "s2.0"
        if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330)\
            or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330):
            if Product_New[j] == 1:
                snNew_ID2.append(Product_ID[j])
                snNew_profit2.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
                    
        if (Product_Type[j] == "PET" and Product_Volume[j] <= 500 and Product_Specialsize[j] == 0):
            if Product_New[j] == 1:
                New_ID3.append(Product_ID[j])
                New_profit3.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
            if product_product_typenum[j] > 3:
                product_product_typenum[j] = 3
        if (Product_Type[j] == "PET" and Product_Volume[j] <= 500 and Product_Specialsize[j] == 1):
            if Product_New[j] == 1:
                sNew_ID3.append(Product_ID[j])
                sNew_profit3.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
            if type(product_product_typenum[j]) == int:
                if product_product_typenum[j] > 3:
                    product_product_typenum[j] = "s3.0"
            elif type(product_product_typenum[j]) == str:
                if int(product_product_typenum[j][1]) > 3:
                    product_product_typenum[j] = "s3.0"
        if (Product_Type[j] == "PET" and Product_Volume[j] <= 500):
            if Product_New[j] == 1:
                snNew_ID3.append(Product_ID[j])
                snNew_profit3.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
                    
        if (Product_Type[j] == "PET" and Product_Volume[j] <= 600 and Product_Specialsize[j] == 0):
            if Product_New[j] == 1:
                New_ID4.append(Product_ID[j])
                New_profit4.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
            if product_product_typenum[j] > 4:
                product_product_typenum[j] = 4
        if (Product_Type[j] == "PET" and Product_Volume[j] <= 600 and Product_Specialsize[j] == 1):
            if Product_New[j] == 1:
                sNew_ID4.append(Product_ID[j])
                sNew_profit4.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j]) #-(setup_cost+replenishment_cost))
            if type(product_product_typenum[j]) == int:
                if product_product_typenum[j] > 4:
                    product_product_typenum[j] = "s4.0"
            elif type(product_product_typenum[j]) == str:
                if int(product_product_typenum[j][1]) > 4:
                    product_product_typenum[j] = "s4.0"
        if (Product_Type[j] == "PET" and Product_Volume[j] <= 600):
            if Product_New[j] == 1:
                snNew_ID4.append(Product_ID[j])
                snNew_profit4.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])#-(setup_cost+replenishment_cost))
                    
        if Product_Type[j] == "PET" and Product_Volume[j] <= 600:
            if Product_New[j] == 1:
                New_ID5.append(Product_ID[j])
                New_profit5.append((Product_Price[j] - Product_Cost[j]) * Product_Product_sales[j])#-(setup_cost+replenishment_cost))
                   
    ##########################################################################
        
    # calculate the numbers and capacity of every cargolane type(0~5)
    for i in range(CargoLane_TotalNumber):                                     
        if type(CargoLane_Type[i]) == float or type(CargoLane_Type[i]) == int:
            if CargoLane_Type[i] == 1:
                Cargolanetype_sum_capacity[1] += CargoLane_Capacity[i]
            elif CargoLane_Type[i] == 2:
                Cargolanetype_sum_capacity[2] += CargoLane_Capacity[i]
            elif CargoLane_Type[i] == 3:
                Cargolanetype_sum_capacity[3] += CargoLane_Capacity[i]
            elif CargoLane_Type[i] == 4:
                Cargolanetype_sum_capacity[4] += CargoLane_Capacity[i]
            elif CargoLane_Type[i] == 5:
                Cargolanetype_sum_capacity[5] += CargoLane_Capacity[i]
            else:
                cargolane_should_empty.append(i)                               # cargolane index!!!!
        else:
            if CargoLane_Type[i][1] == "1":
                Cargolanetype_sum_capacity[1] += CargoLane_Capacity[i]
            elif CargoLane_Type[i][1] == "2":
                Cargolanetype_sum_capacity[2] += CargoLane_Capacity[i]
            elif CargoLane_Type[i][1] == "3":
                Cargolanetype_sum_capacity[3] += CargoLane_Capacity[i]
            elif CargoLane_Type[i][1] == "4":
                Cargolanetype_sum_capacity[4] += CargoLane_Capacity[i]
            elif CargoLane_Type[i][1] == "5":
                Cargolanetype_sum_capacity[5] += CargoLane_Capacity[i]
            else:
                cargolane_should_empty.append(i)                               # cargolane index!!!!
    
    count_type_num = 0
    
    # calculate the average capacity of different cargolane type, it's for calculating the max number of each product
    for j in range(1, len(Cargolanetype_average_capacity)):                    
        if CargoLane_Type.count(j) == 0:
            Cargolanetype_average_capacity[j] = 0
        elif j == 1:
            count_type_num += CargoLane_Type.count(j)
            count_type_num += CargoLane_Type.count("s1.0")
            count_type_num += CargoLane_Type.count("s1")
            Cargolanetype_average_capacity[j] = sum(Cargolanetype_sum_capacity[:j+1]) / count_type_num
        elif j == 2:
            count_type_num += CargoLane_Type.count(j)
            count_type_num += CargoLane_Type.count("s2.0")
            count_type_num += CargoLane_Type.count("s2")
            Cargolanetype_average_capacity[j] = sum(Cargolanetype_sum_capacity[:j+1]) / count_type_num
            # print(Cargolanetype_average_capacity)
        elif j == 3:
            count_type_num = 0
            count_type_num += CargoLane_Type.count(j)
            count_type_num += CargoLane_Type.count("s3.0")
            count_type_num += CargoLane_Type.count("s3")
            Cargolanetype_average_capacity[j] = Cargolanetype_sum_capacity[j] / count_type_num
        elif j == 4:
            count_type_num += CargoLane_Type.count(j)
            count_type_num += CargoLane_Type.count("s4.0")
            count_type_num += CargoLane_Type.count("s4")
            Cargolanetype_average_capacity[j] = sum(Cargolanetype_sum_capacity[3:j+1]) / count_type_num
        else:
            count_type_num += CargoLane_Type.count(j)
            Cargolanetype_average_capacity[j] = sum(Cargolanetype_sum_capacity[3:j+1]) / count_type_num
    
    # calculate the Product_max_cargolanenum
    for i in range(len(Demand_Product_Sales)):
        if demand_product_typenum[i] == 6:
            Product_max_cargolanenum.append(0)
            # print(Product_max_cargolanenum)
        elif demand_product_typenum[i] == 1:
            type_cap = Cargolanetype_average_capacity[2]
            if type_cap != 0:
                Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[2], 0))
            else:
                type_cap = Cargolanetype_average_capacity[1]
                if type_cap != 0:
                    Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[1], 0))
                else:
                    Product_max_cargolanenum.append(0)
        elif demand_product_typenum[i] == 2:
            type_cap = Cargolanetype_average_capacity[2]
            if type_cap != 0:
                Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[2], 0))
            else:
                Product_max_cargolanenum.append(0)

                
        elif demand_product_typenum[i] == 3:
            type_cap = Cargolanetype_average_capacity[5]
            if type_cap != 0:
                Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[5], 0))
            else:
                type_cap = Cargolanetype_average_capacity[4]
                if type_cap != 0:
                    Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[4], 0))
                else:
                    type_cap = Cargolanetype_average_capacity[3]
                    if type_cap != 0:
                        Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[3], 0))
                    else:
                        Product_max_cargolanenum.append(0)
        elif demand_product_typenum[i] == 4:
            type_cap = Cargolanetype_average_capacity[5]
            if type_cap != 0:
                Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[5], 0))
            else:
                type_cap = Cargolanetype_average_capacity[4]
                if type_cap != 0:
                    Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[4], 0))
                else:
                    Product_max_cargolanenum.append(0)
        elif demand_product_typenum[i] == 5:
            type_cap = Cargolanetype_average_capacity[5]
            if type_cap != 0:
                Product_max_cargolanenum.append(round(replenishment_per_time[i] / Cargolanetype_average_capacity[5], 0))
            else:
                Product_max_cargolanenum.append(0)
        # print(Product_max_cargolanenum)
                
    for i in range(len(Product_max_cargolanenum)):
        if Product_max_cargolanenum[i] == 0:
            Product_max_cargolanenum[i] = 1
    
    cargolane_type_num = [0] * 10 # (int(max(CargoLane_Type))+1)
    for i in CargoLane_Type:
        if i == 0 or i == 0.0:
            cargolane_type_num[0] += 1
        elif i == 1 or i == 1.0:
            cargolane_type_num[1] += 1
        elif i == 2 or i == 2.0:
            cargolane_type_num[2] += 1
        elif i == 3 or i == 3.0:
            cargolane_type_num[3] += 1
        elif i == 4 or i == 4.0:
            cargolane_type_num[4] += 1
        elif i == 5 or i == 5.0:
            cargolane_type_num[5] += 1
        elif i == "s1.0" or i == "s1":
            cargolane_type_num[6] += 1
        elif i == "s2.0" or i == "s2":
            cargolane_type_num[7] += 1
        elif i == "s3.0" or i == "s3":
            cargolane_type_num[8] += 1
        elif i == "s4.0" or i == "s4":
            cargolane_type_num[9] += 1
            
    return ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, \
           Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, \
           Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, \
           Product_max_cargolanenum, demand_product_typenum, cargolane_should_empty, cargolane_type_num, \
           New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, \
           product_product_typenum, replenishment_per_time, \
           New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, Cost_CargoLane1, Cost_CargoLane2, Cost_CargoLane3, Cost_CargoLane4, Cost_CargoLane5, \
           sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, \
           sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, \
           sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, \
           sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, \
           sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, \
           snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, \
           snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, \
           snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, \
           snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, \
           snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, \
           setup_cost, replenishment_cost,\
           unit_inventory_cost,unit_backroom_cost,unit_display_cost,unit_ordering_cost

#%%
# declare variables to save info(like ID, price, sales, cost etc) and for recommend product
def classify_recommend_product(Product_ID, Product_Type, Product_Volume, Product_Price, Demand_Product_ID, Product_Cost, setup_cost, replenishment_cost):
    
    recommend_list = []
    for i in Product_ID:                                                       # 將出現在demand中的商品剃除
        recommend_list.append(i)
        # if i in Demand_Product_ID: # demand有的商品不要再推薦
        #     pass
        # else:
        #     recommend_list.append(i)
    
    ID_CargoLane1 = []
    ID_CargoLane2 = []
    ID_CargoLane3 = []
    ID_CargoLane4 = []
    ID_CargoLane5 = []
    
    Price_CargoLane1 = []    
    Price_CargoLane2 = []    
    Price_CargoLane3 = []    
    Price_CargoLane4 = []    
    Price_CargoLane5 = []
    
    Cost_CargoLane1 = []
    Cost_CargoLane2 = []
    Cost_CargoLane3 = []
    Cost_CargoLane4 = []
    Cost_CargoLane5 = []
    
    # s: 清單中只有special
    sID_CargoLane1 = []
    sID_CargoLane2 = []
    sID_CargoLane3 = []
    sID_CargoLane4 = []
    
    sPrice_CargoLane1 = []    
    sPrice_CargoLane2 = []    
    sPrice_CargoLane3 = []    
    sPrice_CargoLane4 = []    
    
    sCost_CargoLane1 = []
    sCost_CargoLane2 = []
    sCost_CargoLane3 = []
    sCost_CargoLane4 = []
    
    # sn: 清單中有special也有一般
    snID_CargoLane1 = []
    snID_CargoLane2 = []
    snID_CargoLane3 = []
    snID_CargoLane4 = []
    
    snPrice_CargoLane1 = []    
    snPrice_CargoLane2 = []    
    snPrice_CargoLane3 = []    
    snPrice_CargoLane4 = []    
    
    snCost_CargoLane1 = []
    snCost_CargoLane2 = []
    snCost_CargoLane3 = []
    snCost_CargoLane4 = []
    
    for i in range(0, len(recommend_list), 1):
        for j in range(0, len(Product_ID), 1):
            if recommend_list[i] == Product_ID[j]:
                if Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0:
                    ID_CargoLane1.append(recommend_list[i])
                    Price_CargoLane1.append(Product_Price[j])
                    Cost_CargoLane1.append(Product_Cost[j])
                    print("1 = ", ID_CargoLane1)
                  
                if Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1:
                    sID_CargoLane1.append(recommend_list[i])
                    sPrice_CargoLane1.append(Product_Price[j])
                    sCost_CargoLane1.append(Product_Cost[j])
                   
                if Product_Type[j] == "CAN" and Product_Volume[j] <= 330:
                    snID_CargoLane1.append(recommend_list[i])
                    snPrice_CargoLane1.append(Product_Price[j])
                    snCost_CargoLane1.append(Product_Cost[j])
                    print("sn = ", snID_CargoLane1)
                   
                    
                if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0) \
                    or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 0):
                    ID_CargoLane2.append(recommend_list[i])
                    Price_CargoLane2.append(Product_Price[j])
                    Cost_CargoLane2.append(Product_Cost[j])
                    print("2 = ", ID_CargoLane2)
                   
                if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1) \
                    or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330 and Product_Specialsize[j] == 1):
                    sID_CargoLane2.append(recommend_list[i])
                    sPrice_CargoLane2.append(Product_Price[j])
                    sCost_CargoLane2.append(Product_Cost[j])
                   
                if (Product_Type[j] == "CAN" and Product_Volume[j] <= 330) \
                    or (Product_Type[j] == "SCAN" and Product_Volume[j] <= 330):
                    snID_CargoLane2.append(recommend_list[i])
                    snPrice_CargoLane2.append(Product_Price[j])
                    snCost_CargoLane2.append(Product_Cost[j])
                    print("sn2 = ", snID_CargoLane2)
                   
                    
                if Product_Type[j] == "PET" and Product_Volume[j] <= 500 and Product_Specialsize[j] == 0:
                    ID_CargoLane3.append(recommend_list[i])
                    Price_CargoLane3.append(Product_Price[j])
                    Cost_CargoLane3.append(Product_Cost[j])
                   
                if Product_Type[j] == "PET" and Product_Volume[j] <= 500 and Product_Specialsize[j] == 1:
                    sID_CargoLane3.append(recommend_list[i])
                    sPrice_CargoLane3.append(Product_Price[j])
                    sCost_CargoLane3.append(Product_Cost[j])
                   
                if Product_Type[j] == "PET" and Product_Volume[j] <= 500:
                    snID_CargoLane3.append(recommend_list[i])
                    snPrice_CargoLane3.append(Product_Price[j])
                    snCost_CargoLane3.append(Product_Cost[j])
                  
                    
                if Product_Type[j] == "PET" and Product_Volume[j] <= 600 and Product_Specialsize[j] == 0:
                    ID_CargoLane4.append(recommend_list[i])
                    Price_CargoLane4.append(Product_Price[j])
                    Cost_CargoLane4.append(Product_Cost[j])
                    
                if Product_Type[j] == "PET" and Product_Volume[j] <= 600 and Product_Specialsize[j] == 1:
                    sID_CargoLane4.append(recommend_list[i])
                    sPrice_CargoLane4.append(Product_Price[j])
                    sCost_CargoLane4.append(Product_Cost[j])
                  
                if Product_Type[j] == "PET" and Product_Volume[j] <= 600:
                    snID_CargoLane4.append(recommend_list[i])
                    snPrice_CargoLane4.append(Product_Price[j])
                    snCost_CargoLane4.append(Product_Cost[j])
                   
                    
                if Product_Type[j] == "PET" and Product_Volume[j] <= 600:
                    ID_CargoLane5.append(recommend_list[i])
                    Price_CargoLane5.append(Product_Price[j])
                    Cost_CargoLane5.append(Product_Cost[j])
                    
    return ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, \
           Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, \
           Cost_CargoLane1, Cost_CargoLane2, Cost_CargoLane3, Cost_CargoLane4, Cost_CargoLane5, \
           sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, \
           sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, \
           sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, \
           snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, \
           snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, \
           snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4


#%%
# saving the current product info
def current_info(Current_Product, Product_ID, Demand_Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, Product_Cost, setup_cost, replenishment_cost):
    Current_ID = []
    Current_price = []
    Current_sales = []
    Current_profit = []
    Current_New = []
    
    Current_occupied = []
    Current_recommended = []
    Current_occupiedlist = []
    
    for ID in Current_Product:
        # print(ID)
        if ID in Product_ID:
            Current_ID.append(ID)
            Current_price.append(Product_Price[Product_ID.index(ID)])
            if ID not in Demand_Product_ID:
                Current_sales.append(Product_Product_sales[Product_ID.index(ID)])
                Current_profit.append((Product_Price[Product_ID.index(ID)] - Product_Cost[Product_ID.index(ID)]) * Product_Product_sales[Product_ID.index(ID)])#-(setup_cost+replenishment_cost))
            else:
                Current_sales.append(Demand_Product_Sales[Demand_Product_ID.index(ID)])
                Current_profit.append((Product_Price[Product_ID.index(ID)] - Product_Cost[Product_ID.index(ID)]) * Demand_Product_Sales[Demand_Product_ID.index(ID)]) #-(setup_cost+replenishment_cost))
            Current_New.append(Product_New[Product_ID.index(ID)])  
        else:
            Current_ID.append("")
            Current_price.append(0)
            Current_sales.append(0)
            Current_profit.append(0)
            Current_New.append(0)
            # Current_occupied = []
            # Current_recommend
    
    for i in range(len(Current_Product)):
        Current_occupiedlist.append(0)
            
    return Current_ID, Current_price, Current_sales, Current_profit, Current_New, Current_occupied, Current_recommended, Current_occupiedlist

#%%
# heuristic solution
def chomosome(ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, cargolane_type_num, Product_New, Product_ID, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, Cost_CargoLane1, Cost_CargoLane2, Cost_CargoLane3, Cost_CargoLane4, Cost_CargoLane5, Recommend_cost1, Recommend_cost2, Recommend_cost3, Recommend_cost4, Recommend_cost5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, modec, Product_Product_sales, setup_cost, replenishment_cost, CargoLane_Diameter_Max_1,Product_Length, unit_inventory_cost,unit_backroom_cost,unit_display_cost,unit_ordering_cost, Product_Cost):
    cargolane_priority = ["s3", "s4", "s1", "s2", 1, 3, 2, 4, 5, 0] #[1, 3, 2, 4, 5, 0]
    #recommended_profit_ratio = 1/5 # will become a variable to modity easily in future
    recommended_profit_ratio = 1
    # for normal
    copy_id_1 = ID_CargoLane1.copy() # CAN
    copy_id_2 = ID_CargoLane2.copy() # SCAN
    copy_id_3 = ID_CargoLane3.copy() # 500PET
    copy_id_4 = ID_CargoLane4.copy() # 600PET
    copy_id_5 = ID_CargoLane5.copy() # TPA
    
    copy_price_1 = Price_CargoLane1.copy()
    copy_price_2 = Price_CargoLane2.copy()
    copy_price_3 = Price_CargoLane3.copy()
    copy_price_4 = Price_CargoLane4.copy()
    copy_price_5 = Price_CargoLane5.copy()
    
    copy_cost_1 = Cost_CargoLane1.copy()
    copy_cost_2 = Cost_CargoLane2.copy()
    copy_cost_3 = Cost_CargoLane3.copy()
    copy_cost_4 = Cost_CargoLane4.copy()
    copy_cost_5 = Cost_CargoLane5.copy()
    
    copy_sales_1 = Sales_CargoLane1.copy()
    copy_sales_2 = Sales_CargoLane2.copy()
    copy_sales_3 = Sales_CargoLane3.copy()
    copy_sales_4 = Sales_CargoLane4.copy()
    copy_sales_5 = Sales_CargoLane5.copy()
    
    
    # s: special
    copy_id_s1 = sID_CargoLane1.copy() # CAN
    copy_id_s2 = sID_CargoLane2.copy() # SCAN
    copy_id_s3 = sID_CargoLane3.copy() # 500PET
    copy_id_s4 = sID_CargoLane4.copy() # 600PET
    
    copy_price_s1 = sPrice_CargoLane1.copy()
    copy_price_s2 = sPrice_CargoLane2.copy()
    copy_price_s3 = sPrice_CargoLane3.copy()
    copy_price_s4 = sPrice_CargoLane4.copy()
    
    copy_cost_s1 = sCost_CargoLane1.copy()
    copy_cost_s2 = sCost_CargoLane2.copy()
    copy_cost_s3 = sCost_CargoLane3.copy()
    copy_cost_s4 = sCost_CargoLane4.copy()
    
    copy_sales_s1 = sSales_CargoLane1.copy()
    copy_sales_s2 = sSales_CargoLane2.copy()
    copy_sales_s3 = sSales_CargoLane3.copy()
    copy_sales_s4 = sSales_CargoLane4.copy()
    
    
    # # let the sales = 0 be 1
    # for i in range(1, 6):
    #     for j in range(len(locals() ["copy_sales_" + str(i)])):
    #         if locals() ["copy_sales_" + str(i)][j] == 0:
    #             locals() ["copy_sales_" + str(i)][j] = 1
                
    # # s: special            
    # for i in range(1, 5):
    #     for j in range(len(locals() ["copy_sales_s" + str(i)])):
    #         if locals() ["copy_sales_s" + str(i)][j] == 0:
    #             locals() ["copy_sales_s" + str(i)][j] = 1

    profit_1 = []
    profit_2 = []
    profit_3 = []
    profit_4 = []
    profit_5 = []
    
    # s: special
    profit_s1 = []
    profit_s2 = []
    profit_s3 = []
    profit_s4 = []
    
    for i in range(len(copy_sales_1)):
        profit_1.append(copy_price_1[i] - copy_cost_1[i])# * copy_sales_1[i]) # - (setup_cost + replenishment_cost))
    for i in range(len(copy_sales_2)):
        profit_2.append(copy_price_2[i] - copy_cost_2[i])# * copy_sales_2[i]) # - (setup_cost + replenishment_cost))
    for i in range(len(copy_sales_3)):
        profit_3.append(copy_price_3[i] - copy_cost_3[i]) #* copy_sales_3[i]) # - (setup_cost + replenishment_cost))
    for i in range(len(copy_sales_4)):
        profit_4.append(copy_price_4[i] - copy_cost_4[i])# * copy_sales_4[i]) # - (setup_cost + replenishment_cost))
    for i in range(len(copy_sales_5)):
        profit_5.append(copy_price_5[i] - copy_cost_5[i]) #* copy_sales_5[i]) # - (setup_cost + replenishment_cost))
    
    # s: special
    for i in range(len(copy_sales_s1)):
        profit_s1.append(copy_price_s1[i] - copy_cost_s1[i]) #* copy_sales_s1[i]) # - (setup_cost + replenishment_cost))
    for i in range(len(copy_sales_s2)):
        profit_s2.append(copy_price_s2[i] - copy_cost_s2[i])# * copy_sales_s2[i]) # - (setup_cost + replenishment_cost))
    for i in range(len(copy_sales_s3)):
        profit_s3.append(copy_price_s3[i] - copy_cost_s3[i])# * copy_sales_s3[i]) #- (setup_cost + replenishment_cost))
    for i in range(len(copy_sales_s4)):
        profit_s4.append(copy_price_s4[i] - copy_cost_s4[i]) #* copy_sales_s4[i]) # - (setup_cost + replenishment_cost))
    #print("p=",profit_2)
    #print(copy_id_1)
    copy_profit_1 = profit_1.copy()
    copy_profit_2 = profit_2.copy()
    copy_profit_3 = profit_3.copy()
    copy_profit_4 = profit_4.copy()
    copy_profit_5 = profit_5.copy()
    
    copy_profit_s1 = profit_s1.copy()
    copy_profit_s2 = profit_s2.copy()
    copy_profit_s3 = profit_s3.copy()
    copy_profit_s4 = profit_s4.copy()
    
    copy_profit_mode1_s1 = profit_s1.copy()
    copy_profit_mode1_s2 = profit_s2.copy()
    copy_profit_mode1_s3 = profit_s3.copy()
    copy_profit_mode1_s4 = profit_s4.copy()
    
    # for new product selection
    copy_New_ID1 = New_ID1.copy()
    copy_New_ID2 = New_ID2.copy()
    copy_New_ID3 = New_ID3.copy()
    copy_New_ID4 = New_ID4.copy()
    copy_New_ID5 = New_ID5.copy()
    
    copy_New_profit1 = New_profit1.copy()
    copy_New_profit2 = New_profit2.copy()
    copy_New_profit3 = New_profit3.copy()
    copy_New_profit4 = New_profit4.copy()
    copy_New_profit5 = New_profit5.copy()
    
    copy_New_IDs1 = snNew_ID1.copy()
    copy_New_IDs2 = snNew_ID2.copy()
    copy_New_IDs3 = snNew_ID3.copy()
    copy_New_IDs4 = snNew_ID4.copy()
    
    copy_New_profits1 = snNew_profit1.copy()
    copy_New_profits2 = snNew_profit2.copy()
    copy_New_profits3 = snNew_profit3.copy()
    copy_New_profits4 = snNew_profit4.copy()
    
    # for mode3 recommend selection 
    recommended_prod = []    
    copy_recommended_id_1 = Recommend_ID1.copy() # CAN
    copy_recommended_id_2 = Recommend_ID2.copy() # SCAN
    copy_recommended_id_3 = Recommend_ID3.copy() # 500PET
    copy_recommended_id_4 = Recommend_ID4.copy() # 600PET
    copy_recommended_id_5 = Recommend_ID5.copy() # TPA
    
    copy2_recommended_id_1 = Recommend_ID1.copy() # CAN
    copy2_recommended_id_2 = Recommend_ID2.copy() # SCAN
    copy2_recommended_id_3 = Recommend_ID3.copy() # 500PET
    copy2_recommended_id_4 = Recommend_ID4.copy() # 600PET
    copy2_recommended_id_5 = Recommend_ID5.copy() # TPA
    
    copy_recommended_price_1 = Recommend_price1.copy()
    copy_recommended_price_2 = Recommend_price2.copy()
    copy_recommended_price_3 = Recommend_price3.copy()
    copy_recommended_price_4 = Recommend_price4.copy()
    copy_recommended_price_5 = Recommend_price5.copy()
    
    copy_recommended_cost_1 = Recommend_cost1.copy()
    copy_recommended_cost_2 = Recommend_cost2.copy()
    copy_recommended_cost_3 = Recommend_cost3.copy()
    copy_recommended_cost_4 = Recommend_cost4.copy()
    copy_recommended_cost_5 = Recommend_cost5.copy()
    
    copy_recommended_profit_1 = [((copy_recommended_price_1[i] - copy_recommended_cost_1[i]) ) for i in range(len(copy_recommended_price_1))]
    copy_recommended_profit_2 = [((copy_recommended_price_2[i] - copy_recommended_cost_2[i]) ) for i in range(len(copy_recommended_price_2))]
    copy_recommended_profit_3 = [((copy_recommended_price_3[i] - copy_recommended_cost_3[i]) ) for i in range(len(copy_recommended_price_3))]
    copy_recommended_profit_4 = [((copy_recommended_price_4[i] - copy_recommended_cost_4[i]) ) for i in range(len(copy_recommended_price_4))]
    copy_recommended_profit_5 = [((copy_recommended_price_5[i] - copy_recommended_cost_5[i]) ) for i in range(len(copy_recommended_price_5))]
    
    copy_recommended_id_s1 = snRecommend_ID1.copy() 
    copy_recommended_id_s2 = snRecommend_ID2.copy()
    copy_recommended_id_s3 = snRecommend_ID3.copy()
    copy_recommended_id_s4 = snRecommend_ID4.copy()
    
    copy2_recommended_id_s1 = snRecommend_ID1.copy()
    copy2_recommended_id_s2 = snRecommend_ID2.copy()
    copy2_recommended_id_s3 = snRecommend_ID3.copy()
    copy2_recommended_id_s4 = snRecommend_ID4.copy()
    
    copy_recommended_price_s1 = snRecommend_price1.copy()
    copy_recommended_price_s2 = snRecommend_price2.copy()
    copy_recommended_price_s3 = snRecommend_price3.copy()
    copy_recommended_price_s4 = snRecommend_price4.copy()
    
    copy_recommended_cost_s1 = snRecommend_cost1.copy()
    copy_recommended_cost_s2 = snRecommend_cost2.copy()
    copy_recommended_cost_s3 = snRecommend_cost3.copy()
    copy_recommended_cost_s4 = snRecommend_cost4.copy()

    copy_recommended_profit_s1 = [((copy_recommended_price_s1[i] - copy_recommended_cost_s1[i]) )  for i in range(len(copy_recommended_price_s1))]
    copy_recommended_profit_s2 = [((copy_recommended_price_s2[i] - copy_recommended_cost_s2[i]) )  for i in range(len(copy_recommended_price_s2))]
    copy_recommended_profit_s3 = [((copy_recommended_price_s3[i] - copy_recommended_cost_s3[i]) )  for i in range(len(copy_recommended_price_s3))]
    copy_recommended_profit_s4 = [((copy_recommended_price_s4[i] - copy_recommended_cost_s4[i]) )  for i in range(len(copy_recommended_price_s4))]
    
    # copy_brand_1 = Brand_CargoLane1.copy()
    # copy_brand_2 = Brand_CargoLane2.copy()
    # copy_brand_3 = Brand_CargoLane3.copy()
    # copy_brand_4 = Brand_CargoLane4.copy()
    # copy_brand_5 = Brand_CargoLane5.copy()
     
    # for mode2 recommend selection 
    copy_id_1_mode2 = ID_CargoLane1.copy()
    copy_id_2_mode2 = ID_CargoLane2.copy()
    copy_id_3_mode2 = ID_CargoLane3.copy()
    copy_id_4_mode2 = ID_CargoLane4.copy()
    copy_id_5_mode2 = ID_CargoLane5.copy()
    
    copy2_id_1_mode2 = ID_CargoLane1.copy()
    copy2_id_2_mode2 = ID_CargoLane2.copy()
    copy2_id_3_mode2 = ID_CargoLane3.copy()
    copy2_id_4_mode2 = ID_CargoLane4.copy()
    copy2_id_5_mode2 = ID_CargoLane5.copy()
    
    copy_price_1_mode2 = Price_CargoLane1.copy()
    copy_price_2_mode2 = Price_CargoLane2.copy()
    copy_price_3_mode2 = Price_CargoLane3.copy()
    copy_price_4_mode2 = Price_CargoLane4.copy()
    copy_price_5_mode2 = Price_CargoLane5.copy()
    
    copy_cost_1_mode2 = Cost_CargoLane1.copy()
    copy_cost_2_mode2 = Cost_CargoLane2.copy()
    copy_cost_3_mode2 = Cost_CargoLane3.copy()
    copy_cost_4_mode2 = Cost_CargoLane4.copy()
    copy_cost_5_mode2 = Cost_CargoLane5.copy()
    
    copy_sales_1_mode2 = Sales_CargoLane1.copy()
    copy_sales_2_mode2 = Sales_CargoLane2.copy()
    copy_sales_3_mode2 = Sales_CargoLane3.copy()
    copy_sales_4_mode2 = Sales_CargoLane4.copy()
    copy_sales_5_mode2 = Sales_CargoLane5.copy()
    
    # # let the sales = 0 be 1
    # for i in range(1, 6):
    #     for j in range(len(locals() ["copy_sales_" + str(i) + "_mode2"])):
    #         if locals() ["copy_sales_" + str(i) + "_mode2"][j] == 0:
    #             locals() ["copy_sales_" + str(i) + "_mode2"][j] = 1
    
    copy_profit_1_mode2 = [(copy_price_1_mode2[i] - copy_cost_1_mode2[i])   for i in range(len(copy_price_1_mode2))]
    copy_profit_2_mode2 = [(copy_price_2_mode2[i] - copy_cost_2_mode2[i])   for i in range(len(copy_price_2_mode2))]
    copy_profit_3_mode2 = [(copy_price_3_mode2[i] - copy_cost_3_mode2[i])   for i in range(len(copy_price_3_mode2))]
    copy_profit_4_mode2 = [(copy_price_4_mode2[i] - copy_cost_4_mode2[i])   for i in range(len(copy_price_4_mode2))]
    copy_profit_5_mode2 = [(copy_price_5_mode2[i] - copy_cost_5_mode2[i])   for i in range(len(copy_price_5_mode2))]
    
    copy_id_s1_mode2 = snID_CargoLane1.copy()
    copy_id_s2_mode2 = snID_CargoLane2.copy()
    copy_id_s3_mode2 = snID_CargoLane3.copy()
    copy_id_s4_mode2 = snID_CargoLane4.copy()
    
    copy2_id_s1_mode2 = snID_CargoLane1.copy()
    copy2_id_s2_mode2 = snID_CargoLane2.copy()
    copy2_id_s3_mode2 = snID_CargoLane3.copy()
    copy2_id_s4_mode2 = snID_CargoLane4.copy()
    
    copy_price_s1_mode2 = snPrice_CargoLane1.copy()
    copy_price_s2_mode2 = snPrice_CargoLane2.copy()
    copy_price_s3_mode2 = snPrice_CargoLane3.copy()
    copy_price_s4_mode2 = snPrice_CargoLane4.copy()
    
    copy_cost_s1_mode2 = snCost_CargoLane1.copy()
    copy_cost_s2_mode2 = snCost_CargoLane2.copy()
    copy_cost_s3_mode2 = snCost_CargoLane3.copy()
    copy_cost_s4_mode2 = snCost_CargoLane4.copy()
    
    copy_sales_s1_mode2 = snSales_CargoLane1.copy()
    copy_sales_s2_mode2 = snSales_CargoLane2.copy()
    copy_sales_s3_mode2 = snSales_CargoLane3.copy()
    copy_sales_s4_mode2 = snSales_CargoLane4.copy()
    
    # # s: special            
    # for i in range(1, 5):
    #     for j in range(len(locals() ["copy_sales_s" + str(i) + "_mode2"])):
    #         if locals() ["copy_sales_s" + str(i) + "_mode2"][j] == 0:
    #             locals() ["copy_sales_s" + str(i) + "_mode2"][j] = 1
    
    copy_profit_s1_mode2 = [(copy_price_s1_mode2[i] - copy_cost_s1_mode2[i])  for i in range(len(copy_price_s1_mode2))]
    copy_profit_s2_mode2 = [(copy_price_s2_mode2[i] - copy_cost_s2_mode2[i]) for i in range(len(copy_price_s2_mode2))]
    copy_profit_s3_mode2 = [(copy_price_s3_mode2[i] - copy_cost_s3_mode2[i])  for i in range(len(copy_price_s3_mode2))]
    copy_profit_s4_mode2 = [(copy_price_s4_mode2[i] - copy_cost_s4_mode2[i])   for i in range(len(copy_price_s4_mode2))]
    
    selection_ID = []                                      
    selection_price = []
    selection_sales = []
    selection_profit = []
    selection_new = []
   
    # remove the conflict one from list
    def cm(replacement_matrix, ranID):  #constraints matrix
        if ranID in replacement_matrix.keys():
            replaceID = replacement_matrix[ranID]
            # delete ID in normal picking product list
            if replaceID in copy_id_1:
                profit_1[copy_id_1.index(replaceID)] = -1
                copy_id_1[copy_id_1.index(replaceID)] = -1
            if replaceID in copy_id_2:
                profit_2[copy_id_2.index(replaceID)] = -1
                copy_id_2[copy_id_2.index(replaceID)] = -1
            if replaceID in copy_id_3:
                profit_3[copy_id_3.index(replaceID)] = -1
                copy_id_3[copy_id_3.index(replaceID)] = -1
            if replaceID in copy_id_4:
                profit_4[copy_id_4.index(replaceID)] = -1
                copy_id_4[copy_id_4.index(replaceID)] = -1
            if replaceID in copy_id_5:
                profit_5[copy_id_5.index(replaceID)] = -1
                copy_id_5[copy_id_5.index(replaceID)] = -1
            # s
            if replaceID in copy_id_s1:
                profit_s1[copy_id_s1.index(replaceID)] = -1
                copy_id_s1[copy_id_s1.index(replaceID)] = -1
            if replaceID in copy_id_s2:
                profit_s2[copy_id_s2.index(replaceID)] = -1
                copy_id_s2[copy_id_s2.index(replaceID)] = -1
            if replaceID in copy_id_s3:
                profit_s3[copy_id_s3.index(replaceID)] = -1
                copy_id_s3[copy_id_s3.index(replaceID)] = -1
            if replaceID in copy_id_s4:
                profit_s4[copy_id_s4.index(replaceID)] = -1
                copy_id_s4[copy_id_s4.index(replaceID)] = -1
            # delete ID in recommanded product list
            if replaceID in copy_recommended_id_1:
                copy_recommended_profit_1[copy_recommended_id_1.index(replaceID)] = -1
                copy_recommended_id_1[copy_recommended_id_1.index(replaceID)] = -1
            if replaceID in copy_recommended_id_2:
                copy_recommended_profit_2[copy_recommended_id_2.index(replaceID)] = -1
                copy_recommended_id_2[copy_recommended_id_2.index(replaceID)] = -1
            if replaceID in copy_recommended_id_3:
                copy_recommended_profit_3[copy_recommended_id_3.index(replaceID)] = -1
                copy_recommended_id_3[copy_recommended_id_3.index(replaceID)] = -1
            if replaceID in copy_recommended_id_4:
                copy_recommended_profit_4[copy_recommended_id_4.index(replaceID)] = -1
                copy_recommended_id_4[copy_recommended_id_4.index(replaceID)] = -1
            if replaceID in copy_recommended_id_5:
                copy_recommended_profit_5[copy_recommended_id_5.index(replaceID)] = -1
                copy_recommended_id_5[copy_recommended_id_5.index(replaceID)] = -1
            # s
            if replaceID in copy_recommended_id_s1:
                copy_recommended_profit_s1[copy_recommended_id_s1.index(replaceID)] = -1
                copy_recommended_id_s1[copy_recommended_id_s1.index(replaceID)] = -1
            if replaceID in copy_recommended_id_s2:
                copy_recommended_profit_s2[copy_recommended_id_s2.index(replaceID)] = -1
                copy_recommended_id_s2[copy_recommended_id_s2.index(replaceID)] = -1
            if replaceID in copy_recommended_id_s3:
                copy_recommended_profit_s3[copy_recommended_id_s3.index(replaceID)] = -1
                copy_recommended_id_s3[copy_recommended_id_s3.index(replaceID)] = -1
            if replaceID in copy_recommended_id_s4:
                copy_recommended_profit_s4[copy_recommended_id_s4.index(replaceID)] = -1
                copy_recommended_id_s4[copy_recommended_id_s4.index(replaceID)] = -1
            # delete ID in new product list
            if replaceID in copy_New_ID1:
                copy_New_profit1[copy_New_ID1.index(replaceID)] = -1
                copy_New_ID1[copy_New_ID1.index(replaceID)] = -1
            if replaceID in copy_New_ID2:
                copy_New_profit2[copy_New_ID2.index(replaceID)] = -1
                copy_New_ID2[copy_New_ID2.index(replaceID)] = -1
            if replaceID in copy_New_ID3:
                copy_New_profit3[copy_New_ID3.index(replaceID)] = -1
                copy_New_ID3[copy_New_ID3.index(replaceID)] = -1
            if replaceID in copy_New_ID4:
                copy_New_profit4[copy_New_ID4.index(replaceID)] = -1
                copy_New_ID4[copy_New_ID4.index(replaceID)] = -1
            if replaceID in copy_New_ID5:
                copy_New_profit5[copy_New_ID5.index(replaceID)] = -1
                copy_New_ID5[copy_New_ID5.index(replaceID)] = -1
            # s
            if replaceID in copy_New_IDs1:
                copy_New_profits1[copy_New_IDs1.index(replaceID)] = -1
                copy_New_IDs1[copy_New_IDs1.index(replaceID)] = -1
            if replaceID in copy_New_IDs2:
                copy_New_profits2[copy_New_IDs2.index(replaceID)] = -1
                copy_New_IDs2[copy_New_IDs2.index(replaceID)] = -1
            if replaceID in copy_New_IDs3:
                copy_New_profits3[copy_New_IDs3.index(replaceID)] = -1
                copy_New_IDs3[copy_New_IDs3.index(replaceID)] = -1
            if replaceID in copy_New_IDs4:
                copy_New_profits4[copy_New_IDs4.index(replaceID)] = -1
                copy_New_IDs4[copy_New_IDs4.index(replaceID)] = -1
                
    for i in Demand_Product_ID:
        cm(replacement_matrix, i)
    
    # select one product from list
    def max_choice(profitlist, IDlist, modec):
        copy_list = profitlist.copy()                                          # 複製變數列表, 如果該列表只有0, return選取的值及其index=0; Copy the variable list, if the list only has 0, return the selected value and its index=0
        if list(set(copy_list)) == [-1]:
            max_ran_x = -1
            max_ran_x_ID = -1
        else:
            if modec == "max":
                max_x = max(profitlist)
            else:
                max_x = choice(profitlist)
                while max_x == -1:
                    max_x = choice(profitlist)                                     # 給假如是randomly picking 用的, 避免隨機選到0的; If it is used for random picking, avoid random selection of 0
            max_ran_x = choice(list(locate(profitlist, lambda x: x == max_x)))       # index: 隨機挑選最大利潤的index; index: Randomly select the index with the maximum profit
            max_ran_x_ID = IDlist[max_ran_x]
        return max_ran_x, max_ran_x_ID                                         # 輸出選擇的index及ID ;  輸出選擇的index及ID
    
    # save the selected one to list
    def select_list(ID_index, ID_index_ID, IDlist, profitlist): # 將選擇的資料放入ID, profit
        selectionlist_ID.append(ID_index_ID)
        selectionlist_profit.append(profitlist[ID_index])
        
    
    # count the selected product number and delete it if meet the max number
    def count_and_delete(max_ran_id, IDlist, profitlist):                   # 輸入在選取list中的index及選取list, 計算選取次數&超出次數刪除; Input the index in the selection list and the selection list, calculate the number of selections & delete the number of times exceeded
        # copy_ID = IDlist[max_ran_index]                                        # ID
        copy_ID = max_ran_id
        
        if copy_ID == -1:
            pass
        elif copy_ID not in Demand_Product_ID:
            pass
        elif selectionlist_ID.count(copy_ID) >= Product_max_cargolanenum[Demand_Product_ID.index(copy_ID)]:
            if copy_ID in copy_id_1:
                profit_1[copy_id_1.index(copy_ID)] = -1
                copy_id_1[copy_id_1.index(copy_ID)] = -1
            if copy_ID in copy_id_2:
                profit_2[copy_id_2.index(copy_ID)] = -1
                copy_id_2[copy_id_2.index(copy_ID)] = -1
            if copy_ID in copy_id_3:
                profit_3[copy_id_3.index(copy_ID)] = -1
                copy_id_3[copy_id_3.index(copy_ID)] = -1
            if copy_ID in copy_id_4:
                profit_4[copy_id_4.index(copy_ID)] = -1
                copy_id_4[copy_id_4.index(copy_ID)] = -1
            if copy_ID in copy_id_5:
                profit_5[copy_id_5.index(copy_ID)] = -1
                copy_id_5[copy_id_5.index(copy_ID)] = -1
            # s
            if copy_ID in copy_id_s1:
                profit_s1[copy_id_s1.index(copy_ID)] = -1
                copy_id_s1[copy_id_s1.index(copy_ID)] = -1
            if copy_ID in copy_id_s2:
                profit_s2[copy_id_s2.index(copy_ID)] = -1
                copy_id_s2[copy_id_s2.index(copy_ID)] = -1
            if copy_ID in copy_id_s3:
                profit_s3[copy_id_s3.index(copy_ID)] = -1
                copy_id_s3[copy_id_s3.index(copy_ID)] = -1
            if copy_ID in copy_id_s4:
                profit_s4[copy_id_s4.index(copy_ID)] = -1
                copy_id_s4[copy_id_s4.index(copy_ID)] = -1
    
    # definiton for normal product selection
    def pick_list(idlist, profitlist, modec):
        max_ran, max_ran_ID = max_choice(profitlist, idlist, modec)
        select_list(max_ran, max_ran_ID, idlist, profitlist)
        cm(replacement_matrix, max_ran_ID)
        count_and_delete(max_ran_ID, idlist, profitlist) 
    
    # definiton for new product selection
    def pick_list_newprod(newlist, newprofit, selectionlistID, selectionlistprofit, idlist, profitlist): # 已於呼叫時判斷不為0及[]; It has been judged not to be 0 and [] when calling
        newpick_index = newprofit.index(max(newprofit))
        newpick = newlist[newpick_index]
        # indexofnewpick = idlist.index(newpick)
        # select_list(indexofnewpick, newpick, idlist, profitlist)
        indexofnewpick = newlist.index(newpick)
        select_list(indexofnewpick, newpick, newlist, newprofit)
        cm(replacement_matrix, newpick)
        # count_and_delete(idlist.index(newpick), idlist, profitlist) # copy_id_list還是會計算是否大於該選貨道數
        count_and_delete(newpick, idlist, profitlist) # copy_id_list還是會計算是否大於該選貨道數
        if newpick not in Demand_Product_ID:
            pass
        elif selectionlistID.count(newpick) >= Product_max_cargolanenum[Demand_Product_ID.index(newpick)]:
            if newpick in copy_New_ID1:
                copy_New_profit1[copy_New_ID1.index(newpick)] = -1
                copy_New_ID1[copy_New_ID1.index(newpick)] = -1
            if newpick in copy_New_ID2:
                copy_New_profit2[copy_New_ID2.index(newpick)] = -1
                copy_New_ID2[copy_New_ID2.index(newpick)] = -1
            if newpick in copy_New_ID3:
                copy_New_profit3[copy_New_ID3.index(newpick)] = -1
                copy_New_ID3[copy_New_ID3.index(newpick)] = -1
            if newpick in copy_New_ID4:
                copy_New_profit4[copy_New_ID4.index(newpick)] = -1
                copy_New_ID4[copy_New_ID4.index(newpick)] = -1
            if newpick in copy_New_ID5:
                copy_New_profit5[copy_New_ID5.index(newpick)] = -1
                copy_New_ID5[copy_New_ID5.index(newpick)] = -1
            # s
            if newpick in copy_New_IDs1:
                copy_New_profits1[copy_New_IDs1.index(newpick)] = -1
                copy_New_IDs1[copy_New_IDs1.index(newpick)] = -1
            if newpick in copy_New_IDs2:
                copy_New_profits2[copy_New_IDs2.index(newpick)] = -1
                copy_New_IDs2[copy_New_IDs2.index(newpick)] = -1
            if newpick in copy_New_IDs3:
                copy_New_profits3[copy_New_IDs3.index(newpick)] = -1
                copy_New_IDs3[copy_New_IDs3.index(newpick)] = -1
            if newpick in copy_New_IDs4:
                copy_New_profits4[copy_New_IDs4.index(newpick)] = -1
                copy_New_IDs4[copy_New_IDs4.index(newpick)] = -1
            # newlist[newlist.index(newpick)] = 0
    
    # definiton for recommend product selection
    def pick_list_recommend(idlist, variablelist, pickmode, idlist2):
        
        def max_rec(IDlis, variable_list, pickmode, IDlis2): # 輸出選取值ID及index; # Output selected value ID and index
            copy_vl = variable_list.copy()
            if pickmode == "max":
                if mode == str(2):
                    cargolane_num_list = [Product_max_cargolanenum[Demand_Product_ID.index(IDlis2[x])] for x in range(len(IDlis2))]
                    edge_profit_vl = [copy_vl[i] / cargolane_num_list[i] for i in range(len(copy_vl))]
                    max_p = copy_vl[edge_profit_vl.index(max(edge_profit_vl))]
                else:                    
                    max_p = max(copy_vl) # 原本的程式
            else:
                if list(set(copy_vl)) == [-1]:
                    max_p = -1
                else:
                    max_p = choice(copy_vl)
                    while max_p == -1:
                        max_p = choice(copy_vl)
            max_p_index = variable_list.index(max_p)
            max_p_ID = IDlis[max_p_index]
            recommended_prod.append(max_p_ID)
            return max_p_ID, max_p_index
        
        def delete_all_list(IDlist, variablelist, ID_index, ID):
            # copy_ID = ID.copy()
            if ID == -1:
                pass
            elif mode == str(2) and recommended_prod.count(ID) >= 2:
                if ID in copy_id_1_mode2:
                    copy_profit_1_mode2[copy_id_1_mode2.index(ID)] = -1
                    copy_id_1_mode2[copy_id_1_mode2.index(ID)] = -1
                if ID in copy_id_2_mode2:
                    copy_profit_2_mode2[copy_id_2_mode2.index(ID)] = -1
                    copy_id_2_mode2[copy_id_2_mode2.index(ID)] = -1
                if ID in copy_id_3_mode2:
                    copy_profit_3_mode2[copy_id_3_mode2.index(ID)] = -1
                    copy_id_3_mode2[copy_id_3_mode2.index(ID)] = -1
                if ID in copy_id_4_mode2:
                    copy_profit_4_mode2[copy_id_4_mode2.index(ID)] = -1
                    copy_id_4_mode2[copy_id_4_mode2.index(ID)] = -1
                if ID in copy_id_5_mode2:
                    copy_profit_5_mode2[copy_id_5_mode2.index(ID)] = -1
                    copy_id_5_mode2[copy_id_5_mode2.index(ID)] = -1
                # s
                if ID in copy_id_s1_mode2:
                    copy_profit_s1_mode2[copy_id_s1_mode2.index(ID)] = -1
                    copy_id_s1_mode2[copy_id_s1_mode2.index(ID)] = -1
                if ID in copy_id_s2_mode2:
                    copy_profit_s2_mode2[copy_id_s2_mode2.index(ID)] = -1
                    copy_id_s2_mode2[copy_id_s2_mode2.index(ID)] = -1
                if ID in copy_id_s3_mode2:
                    copy_profit_s3_mode2[copy_id_s3_mode2.index(ID)] = -1
                    copy_id_s3_mode2[copy_id_s3_mode2.index(ID)] = -1
                if ID in copy_id_s4_mode2:
                    copy_profit_s4_mode2[copy_id_s4_mode2.index(ID)] = -1
                    copy_id_s4_mode2[copy_id_s4_mode2.index(ID)] = -1
            elif mode == str(3) and recommended_prod.count(ID) >= 2:
                if ID in copy_recommended_id_1:
                    copy_recommended_profit_1[copy_recommended_id_1.index(ID)] = -1
                    copy_recommended_id_1[copy_recommended_id_1.index(ID)] = -1
                if ID in copy_recommended_id_2:
                    copy_recommended_profit_2[copy_recommended_id_2.index(ID)] = -1
                    copy_recommended_id_2[copy_recommended_id_2.index(ID)] = -1
                if ID in copy_recommended_id_3:
                    copy_recommended_profit_3[copy_recommended_id_3.index(ID)] = -1
                    copy_recommended_id_3[copy_recommended_id_3.index(ID)] = -1
                if ID in copy_recommended_id_4:
                    copy_recommended_profit_4[copy_recommended_id_4.index(ID)] = -1
                    copy_recommended_id_4[copy_recommended_id_4.index(ID)] = -1
                if ID in copy_recommended_id_5:
                    copy_recommended_profit_5[copy_recommended_id_5.index(ID)] = -1
                    copy_recommended_id_5[copy_recommended_id_5.index(ID)] = -1
                # s
                if ID in copy_recommended_id_s1:
                    copy_recommended_profit_s1[copy_recommended_id_s1.index(ID)] = -1
                    copy_recommended_id_s1[copy_recommended_id_s1.index(ID)] = -1
                if ID in copy_recommended_id_s2:
                    copy_recommended_profit_s2[copy_recommended_id_s2.index(ID)] = -1
                    copy_recommended_id_s2[copy_recommended_id_s2.index(ID)] = -1
                if ID in copy_recommended_id_s3:
                    copy_recommended_profit_s3[copy_recommended_id_s3.index(ID)] = -1
                    copy_recommended_id_s3[copy_recommended_id_s3.index(ID)] = -1
                if ID in copy_recommended_id_s4:
                    copy_recommended_profit_s4[copy_recommended_id_s4.index(ID)] = -1
                    copy_recommended_id_s4[copy_recommended_id_s4.index(ID)] = -1
        
        def select_rec(IDlist, variable_list, index, index_ID):
            if IDlist[index] == -1:
                selectionlist_ID.append("")
                selectionlist_profit.append(0)
            else:
                selectionlist_ID.append(IDlist[index])
                selectionlist_profit.append(variable_list[index])
        
        max_p_ID, max_p_index = max_rec(idlist, variablelist, pickmode, idlist2)
        select_rec(idlist, variablelist, max_p_index, max_p_ID)
        cm(replacement_matrix, max_p_ID)
        delete_all_list(idlist, variablelist, max_p_index, max_p_ID)

    # definiton for make sure the min number of product selected
    choose_priority = {1:1, 2:2, 3:3, 4:4, 5:5, "s1.0":1.5, "s2.0":2.5, "s3.0":3.5, "s4.0":4.5, 4.5:"s4.0", 3.5:"s3.0", 2.5:"s2.0", 1.5:"s1.0"}
    def min_sku(selectionlist, num, modec, occupied):                                           # 最少需要幾個商品
        copy_selectionlist = selectionlist.copy()
        
        copy_copy_selectionlist = copy_selectionlist.copy()
        
        for i in range(len(copy_copy_selectionlist)):
            if occupied[i] == 1:
                copy_copy_selectionlist[i] = ""
        
        sku_num = list(set(copy_copy_selectionlist))
        prod_morethan1 = []                                                    # 佔>1貨道的商品 #Commodities occupying >1 aisle
        prod_morethan1_type = []                                               # 佔>1貨道的商品類別 #Commodity categories that account for >1 aisle
        havenot_choose = []                                                    # 尚未被選過的商品(demand中) #Products that have not been selected yet (in demand)
        havenot_choose_type = []
        prod_morethan1_cargolanetype = [] 
        prod_morethan1_cargolanetype_index = [] 
        
        while "" in sku_num:
            sku_num.remove("")
        while 0 in sku_num:
            sku_num.remove(0)
        while -1 in sku_num:
            sku_num.remove(-1)
        
        for i in sku_num:
            if copy_selectionlist.count(i) > 1:
                prod_morethan1.append(i)
                prod_morethan1_type.append(product_product_typenum[Product_ID.index(i)])
                prod_morethan1_cargolanetype.append(list(locate(copy_selectionlist, lambda x: x == i)))
                prod_morethan1_cargolanetype_index.append(list(locate(copy_selectionlist, lambda x: x == i)))
                
        for kk in range(len(prod_morethan1_cargolanetype)):
            for jj in range(len(prod_morethan1_cargolanetype[kk])):
                prod_morethan1_cargolanetype[kk][jj] = selection_inwhichcargolanetype[prod_morethan1_cargolanetype[kk][jj]]
        
        for j in Demand_Product_ID:
            if j in sku_num:
                pass
            else:
                havenot_choose.append(j)
                havenot_choose_type.append(product_product_typenum[Product_ID.index(j)])
        #####
        for i in range(len(havenot_choose_type)):
            havenot_choose_type[i] = choose_priority[havenot_choose_type[i]]
            
        pp = pd.DataFrame({"ID": havenot_choose, "type": havenot_choose_type})
        pppp = pp.sort_values(by = ["type"], ascending = False)
        havenot_choose = pppp["ID"].tolist()
        havenot_choose_type = pppp["type"].tolist()
        
        for i in range(len(havenot_choose_type)):
            havenot_choose_type[i] = choose_priority[havenot_choose_type[i]]
        #####
        def pre_cal():
            copy_copy_selectionlist_ = copy_selectionlist.copy()
            
            for i in range(len(copy_copy_selectionlist_)):
                if occupied[i] == 1:
                    copy_copy_selectionlist_[i] = 0
                    
            sku_num_ = list(set(copy_copy_selectionlist_))
            prod_morethan1_ = []                                                    # 佔>1貨道的商品 #Commodities occupying >1 aisle
            prod_morethan1_type_ = []                                               # 佔>1貨道的商品類別 #Commodity categories that account for >1 aisle
            havenot_choose_ = []                                                    # 尚未被選過的商品(demand中) #Products that have not been selected yet (in demand)
            havenot_choose_type_ = []
            prod_morethan1_cargolanetype_ = [] 
            prod_morethan1_cargolanetype_index_ = [] 
        
            while "" in sku_num_:
                sku_num_.remove("")
            while 0 in sku_num_:
                sku_num_.remove(0)
            while -1 in sku_num_:
                sku_num_.remove(-1)
        
            for i in sku_num_:
                if copy_selectionlist.count(i) > 1:
                    prod_morethan1_.append(i)
                    prod_morethan1_type_.append(product_product_typenum[Product_ID.index(i)])
                    prod_morethan1_cargolanetype_.append(list(locate(copy_selectionlist, lambda x: x == i)))
                    prod_morethan1_cargolanetype_index_.append(list(locate(copy_selectionlist, lambda x: x == i)))
                
            for kk in range(len(prod_morethan1_cargolanetype_)):
                for jj in range(len(prod_morethan1_cargolanetype_[kk])):
                    prod_morethan1_cargolanetype_[kk][jj] = selection_inwhichcargolanetype[prod_morethan1_cargolanetype_[kk][jj]]
        
            for i in Demand_Product_ID:
                if i in sku_num_:
                    pass
                else:
                    havenot_choose_.append(i)
                    havenot_choose_type_.append(product_product_typenum[Product_ID.index(i)])
            #####
            for i in range(len(havenot_choose_type_)):
                havenot_choose_type_[i] = choose_priority[havenot_choose_type_[i]]
            
            ppp = pd.DataFrame({"ID": havenot_choose_, "type": havenot_choose_type_})
            ppppp = ppp.sort_values(by = ["type"], ascending = False)
            havenot_choose_ = ppppp["ID"].tolist()
            havenot_choose_type_ = ppppp["type"].tolist()
            
            for i in range(len(havenot_choose_type_)):
                havenot_choose_type_[i] = choose_priority[havenot_choose_type_[i]] 
            #####
                    
            return sku_num_, prod_morethan1_, prod_morethan1_type_, havenot_choose_, havenot_choose_type_, prod_morethan1_cargolanetype_, prod_morethan1_cargolanetype_index_
        
        if modec == "max":
            times = 1
            while len(sku_num) < num:
                ranchoice = havenot_choose[0] # 在未被選中的list選取一個
                if times >= 5:
                    break
                
                typeofchoosen = [prod_morethan1_cargolanetype[j][m] for j in range(len(prod_morethan1_cargolanetype)) for m in range(len(prod_morethan1_cargolanetype[j]))]
                typeofchoosen_index = [prod_morethan1_cargolanetype_index[j][m] for j in range(len(prod_morethan1_cargolanetype_index)) for m in range(len(prod_morethan1_cargolanetype_index[j]))]            
                    
                define = []
                for i in list(set(typeofchoosen)):
                    if type(havenot_choose_type[havenot_choose.index(ranchoice)]) == str:
                        if i not in prod_cargo[int(havenot_choose_type[havenot_choose.index(ranchoice)][1]) + 5]:
                            define.append(0)
                        else:
                            define.append(1)
                    else:
                        if i not in prod_cargo[havenot_choose_type[havenot_choose.index(ranchoice)]]:
                            define.append(0)
                        else:
                            define.append(1)
                
                if list(set(define)) == [0] or list(set(define)) == []:
                    times += 1
                    continue
                else:
                    # typeofchoosen = [prod_morethan1_cargolanetype[j][m] for j in range(len(prod_morethan1_cargolanetype)) for m in range(len(prod_morethan1_cargolanetype[j]))]
                    # typeofchoosen_index = [prod_morethan1_cargolanetype_index[j][m] for j in range(len(prod_morethan1_cargolanetype_index)) for m in range(len(prod_morethan1_cargolanetype_index[j]))]            
                    
                    if (havenot_choose_type[havenot_choose.index(ranchoice)] == 1) and (1 in typeofchoosen or 2 in typeofchoosen or "s1" in typeofchoosen or "s2" in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 1 or x == "s1" or x == 2 or x == "s2"))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 2) and (2 in typeofchoosen or "s2" in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 2 or x == "s2"))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 3) and (3 in typeofchoosen or 4 in typeofchoosen or 5 in typeofchoosen or "s3" in typeofchoosen or "s4" in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 3 or x == 4 or x == 5 or x == "s3" or x == "s4"))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 4) and (4 in typeofchoosen or "s4" in typeofchoosen or 5 in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 4 or x == 5 or x == "s4"))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 5) and (5 in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 5))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s1.0") and ("s1" in typeofchoosen or "s2" in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s1" or x == "s2"))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s2.0") and ("s2" in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s2"))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s3.0") and ("s3" in typeofchoosen or "s4" in typeofchoosen or 5 in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s3" or x == "s4" or x == 5))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s4.0") and ("s4" in typeofchoosen or 5 in typeofchoosen):
                        candidate = [typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s4" or x == 5))][-1]
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
        else:
            times = 1
            while len(sku_num) < num:
                ranchoice = choice(havenot_choose) # 在未被選中的list選取一個
                if times >= 10:
                    break
                
                typeofchoosen = [prod_morethan1_cargolanetype[j][m] for j in range(len(prod_morethan1_cargolanetype)) for m in range(len(prod_morethan1_cargolanetype[j]))]
                typeofchoosen_index = [prod_morethan1_cargolanetype_index[j][m] for j in range(len(prod_morethan1_cargolanetype_index)) for m in range(len(prod_morethan1_cargolanetype_index[j]))]            
                    
                define = []
                for i in list(set(typeofchoosen)):
                    if type(havenot_choose_type[havenot_choose.index(ranchoice)]) == str:
                        if i not in prod_cargo[int(havenot_choose_type[havenot_choose.index(ranchoice)][1]) + 5]:
                            define.append(0)
                        else:
                            define.append(1)
                    else:
                        if i not in prod_cargo[havenot_choose_type[havenot_choose.index(ranchoice)]]:
                            define.append(0)
                        else:
                            define.append(1)
                
                if list(set(define)) == [0] or list(set(define)) == []:
                    times += 1
                    continue
                else:
                    # typeofchoosen = [prod_morethan1_cargolanetype[j][m] for j in range(len(prod_morethan1_cargolanetype)) for m in range(len(prod_morethan1_cargolanetype[j]))]
                    # typeofchoosen_index = [prod_morethan1_cargolanetype_index[j][m] for j in range(len(prod_morethan1_cargolanetype_index)) for m in range(len(prod_morethan1_cargolanetype_index[j]))]            
                    
                    if (havenot_choose_type[havenot_choose.index(ranchoice)] == 1) and (1 in typeofchoosen or 2 in typeofchoosen or "s1" in typeofchoosen or "s2" in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 1 or x == "s1" or x == 2 or x == "s2"))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 2) and (2 in typeofchoosen or "s2" in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 2 or x == "s2"))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 3) and (3 in typeofchoosen or 4 in typeofchoosen or 5 in typeofchoosen or "s3" in typeofchoosen or "s4" in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 3 or x == 4 or x == 5 or x == "s3" or x == "s4"))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 4) and (4 in typeofchoosen or "s4" in typeofchoosen or 5 in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 4 or x == 5 or x == "s4"))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 5) and (5 in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == 5))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s1.0") and ("s1" in typeofchoosen or "s2" in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s1" or x == "s2"))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s2.0") and ("s2" in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s2"))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s3.0") and ("s3" in typeofchoosen or "s4" in typeofchoosen or 5 in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s3" or x == "s4" or x == 5))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                    elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s4.0") and ("s4" in typeofchoosen or 5 in typeofchoosen):
                        candidate = choice([typeofchoosen_index[i] for i in list(locate(typeofchoosen, lambda x: x == "s4" or x == 5))])
                        copy_selectionlist[candidate] = ranchoice
                        sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
            
                # define = []
                # for i in prod_morethan1_type:
                #     if type(havenot_choose_type[havenot_choose.index(ranchoice)]) == str:
                #         if i not in prod_cargo[int(havenot_choose_type[havenot_choose.index(ranchoice)][1]) + 5]:
                #             define.append(0)
                #         else:
                #             define.append(1)
                #     else:
                #         if i not in prod_cargo[havenot_choose_type[havenot_choose.index(ranchoice)]]:
                #             define.append(0)
                #         else:
                #             define.append(1)
                            
                # if list(set(define)) == [0] or list(set(define)) == []:
                #     times += 1
                #     continue
                # else:
                #     if (havenot_choose_type[havenot_choose.index(ranchoice)] == 1) and (1 in prod_morethan1_type or 2 in prod_morethan1_type or "s1.0" in prod_morethan1_type or "s2.0" in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == 1 or x == "s1.0" or x == 2 or x == "s2.0"))) # 判別type然後取出index
                #         replacement_ID = prod_morethan1[replacement] # 要取代掉的ID
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1] # 取最後一個欄位來擺放新品, 為了貨道相鄰
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 2) and (2 in prod_morethan1_type or "s2.0" in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == 2 or x == "s2.0")))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 3) and (3 in prod_morethan1_type or 4 in prod_morethan1_type or 5 in prod_morethan1_type or "s3.0" in prod_morethan1_type or "s4.0" in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == 3 or x == "s3.0" or x == 4 or x == "s4.0" or x == 5)))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 4) and (4 in prod_morethan1_type or "s4.0" in prod_morethan1_type or 5 in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == 4 or x == "s4.0" or x == 5)))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == 5) and (5 in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == 5)))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s1.0") and ("s1.0" in prod_morethan1_type or "s2.0" in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == "s1.0" or x == "s2.0")))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s2.0") and ("s2.0" in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == "s2.0")))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s3.0") and ("s3.0" in prod_morethan1_type or "s4.0" in prod_morethan1_type or 5 in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == "s3.0" or x == "s4.0" or x == 5)))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
                #     elif (havenot_choose_type[havenot_choose.index(ranchoice)] == "s4.0") and ("s4.0" in prod_morethan1_type or 5 in prod_morethan1_type):
                #         replacement = choice(list(locate(prod_morethan1_type, lambda x: x == "s4.0" or x == 5)))
                #         replacement_ID = prod_morethan1[replacement]
                #         candidate = list(locate(copy_selectionlist, lambda x: x == replacement_ID))[-1]
                #         copy_selectionlist[candidate] = ranchoice
                #         sku_num, prod_morethan1, prod_morethan1_type, havenot_choose, havenot_choose_type, prod_morethan1_cargolanetype, prod_morethan1_cargolanetype_index = pre_cal()
            
        return copy_selectionlist
    
    # prod_cargo = [[0], [1, 2], [2], [3, 4, 5], [4, 5], [5]]
    prod_cargo = [[0], [1, 2, "s1", "s2"], [2, "s2"], [3, 4, 5, "s3", "s4"], [4, 5, "s4"], [5], ["s1", "s2"], ["s2"], ["s3", "s4"], ["s4"]]
    selection_inwhichcargolanetype = [] # 存取該品項是在哪一個type被選到的 # Which type is selected to access the item
    numprod = 0
    cargolane_occupied = [] # Cargolane ID
    
    atleast = math.ceil(len(CargoLane_ID) * (new_prod_ratio / 100)) # 新品最少需要幾個貨道 #At least how many lanes are required for new products
    for i in range(len(Product_New)): # 如果是新品的話, Product_max_cargolane次數增加atleast次數 #If it is a new product, the number of Product_max_cargolane increases atleast times
        if Product_New[i] == 1 and Product_ID[i] in Demand_Product_ID:
            Product_max_cargolanenum[Demand_Product_ID.index(Product_ID[i])] += atleast
    
    # prodcut selection
    selectionlist_ID = []                                     
    selectionlist_price = []
    selectionlist_sales = []
    selectionlist_profit = []
    selectionlist_new = []
    for i in cargolane_priority: # 照商品順序挑選[s3, s4, s1, s2, 1, 3, 2, 4, 5, 0] # Select in order [s3, s4, s1, s2, 1, 3, 2, 4, 5, 0]
        if i == "s1":
            i = 6
        elif i == "s2":
            i = 7
        elif i == "s3":
            i = 8
        elif i == "s4":
            i = 9
        for j in range(cargolane_type_num[i]): # 每個類別挑選幾次 # Select several times for each category
            if i == 6:
                i = "s1"
            elif i == 7:
                i = "s2"
            elif i == 8:
                i = "s3"
            elif i == 9:
                i = "s4"
            if i == 0:
                selectionlist_ID.append("")
                selectionlist_profit.append(0)
                selection_inwhichcargolanetype.append(i)
                cargolane_occupied.append(0)
                
            # 假設s沒有品項可選, 直接讓s的貨道去選一般品項 Assuming that s has no items to choose from, just let s’s aisle choose general items
            elif list(set(locals() ["profit_" + str(i)])) == [] and type(i) == str and list(set(locals() ["profit_" + str(i)[1]])) != [-1] and list(set(locals() ["profit_" + str(i)[1]])) != []:
                pick_list(locals() ["copy_id_" + str(i)[1]], locals() ["profit_" + str(i)[1]], modec)
                selection_inwhichcargolanetype.append(i)
                cargolane_occupied.append(0) # 0=不是推薦品項 # 0=not a recommended item
                
            elif list(set(locals() ["profit_" + str(i)])) != [-1] and list(set(locals() ["profit_" + str(i)])) != []: # profit_i 不等於0, 代表該品項仍有商品可以選取
                # list(set(Product_New)) != [0]: # 有新品才選 Only when there are new products
                if list(set(Product_New)) != [0] and locals() ["copy_New_ID" + str(i)] != [] and list(set(locals() ["copy_New_ID" + str(i)])) != [-1] and numprod < atleast: # 如果新品項清單不等於空值或0, 且新品數少於需求, 就先選新品
                    pick_list_newprod(locals() ["copy_New_ID" + str(i)], locals() ["copy_New_profit" + str(i)], selectionlist_ID, selectionlist_profit, locals() ["copy_id_" + str(i)], locals() ["profit_" + str(i)])
                    numprod += 1
                else:
                    pick_list(locals() ["copy_id_" + str(i)], locals() ["profit_" + str(i)], modec)

                selection_inwhichcargolanetype.append(i)
                cargolane_occupied.append(0) # 0=不是推薦品項 # 0=not a recommended item
            
            # s 的被選完了, 如果i = sx & 該s 的一般尺寸貨道還有品項可以選, s就去選一般的(沒s) !!!!! # s has been selected, if i = sx & there are still items to choose from in the general size aisle of the s, s will choose the general (no s)!!!!!
            elif list(set(locals() ["profit_" + str(i)])) == [-1] and type(i) == str and list(set(locals() ["profit_" + str(i)[1]])) != [-1] and list(set(locals() ["profit_" + str(i)[1]])) != []:
                pick_list(locals() ["copy_id_" + str(i)[1]], locals() ["profit_" + str(i)[1]], modec)
                selection_inwhichcargolanetype.append(i)
                cargolane_occupied.append(0) # 0=不是推薦品項 # 0=not a recommended item
                
            elif list(set(locals() ["profit_" + str(i)])) == [-1] or list(set(locals() ["profit_" + str(i)])) == []: # profit_i 等於0, 代表該品項皆被選完, 所以選擇推薦品項 # profit_i is equal to 0, which means that the item has been selected, so choose the recommended item
                if mode == str(1):
                    selectionlist_ID.append("")
                    cargolane_occupied.append(0)
                elif mode == str(2):
                    if locals() ["copy_id_" + str(i) + "_mode2"] != []:#
                        pick_list_recommend(locals() ["copy_id_" + str(i) + "_mode2"], locals() ["copy_profit_" + str(i) + "_mode2"], "max", locals() ["copy2_id_" + str(i) + "_mode2"])
                        if selectionlist_ID[-1] == "":
                            cargolane_occupied.append(0) 
                        else:
                            cargolane_occupied.append(1)
                    else:#
                        selectionlist_ID.append("")#
                        cargolane_occupied.append(0)#
                elif mode == str(3):
                    if locals() ["copy_recommended_id_" + str(i)] != []:#
                        pick_list_recommend(locals() ["copy_recommended_id_" + str(i)], locals() ["copy_recommended_profit_" + str(i)], "max", locals() ["copy_recommended_id_" + str(i)])
                        if selectionlist_ID[-1] == "":
                            cargolane_occupied.append(0)
                        else:
                            cargolane_occupied.append(1)
                    else:#
                        selectionlist_ID.append("")#
                        cargolane_occupied.append(0)#    
                selection_inwhichcargolanetype.append(i)

    selectionlist_ID = min_sku(selectionlist_ID, sku_min_num, modec, cargolane_occupied) #sku_min_num

    # cargolane assignment
    selectionlist_sorted = []
    cargolane_empty = []
    for i in [0, 1, 2, 3, 4, 5, 's1', 's2', 's3', 's4']:
        sel_sort = []
        sel_sort_sales = []
        sel_sort_rev = []
        for h in list(locate(selection_inwhichcargolanetype, lambda x: x == i)):
            if cargolane_occupied[h] == 1:
                sel_sort.append(selectionlist_ID[h] + "_")
                if mode == str(1):
                    sel_sort_sales.append(-9999999999)
                    sel_sort_rev.append(-9999999999)
                elif mode == str(2):
                    sel_sort_sales.append(Demand_Product_Sales[Demand_Product_ID.index(selectionlist_ID[h])])
                    sel_sort_rev.append(((Product_Price[Product_ID.index(selectionlist_ID[h])] - Product_Cost[Product_ID.index(selectionlist_ID[h])]) * Product_max_cargolanenum[Demand_Product_ID.index(selectionlist_ID[h])])) # - (setup_cost + replenishment_cost))
                else:
                    sel_sort_sales.append(-9999999999 + Product_Product_sales[Product_ID.index(selectionlist_ID[h])])
                    sel_sort_rev.append(-9999999999 + ((Product_Price[Product_ID.index(selectionlist_ID[h])] - Product_Cost[Product_ID.index(selectionlist_ID[h])]) * Product_Product_sales[Product_ID.index(selectionlist_ID[h])])) # - (setup_cost + replenishment_cost))
            else:
                if selectionlist_ID[h] == "":
                    sel_sort.append("zzzzzz")
                    sel_sort_sales.append(-9)
                    sel_sort_rev.append(-9)
                else:
                    sel_sort.append(selectionlist_ID[h])
                    if selectionlist_ID[h] in Demand_Product_ID:
                        sel_sort_sales.append(Demand_Product_Sales[Demand_Product_ID.index(selectionlist_ID[h])])
                        sel_sort_rev.append((Product_Price[Product_ID.index(selectionlist_ID[h])] - Product_Cost[Product_ID.index(selectionlist_ID[h])]) * Demand_Product_Sales[Demand_Product_ID.index(selectionlist_ID[h])]) # - (setup_cost + replenishment_cost))
                        #print("sel1=", Product_Product_sales[Product_ID.index(selectionlist_ID[h])])
                    else:
                        sel_sort_sales.append(Product_Product_sales[Product_ID.index(selectionlist_ID[h])])
                        sel_sort_rev.append((Product_Price[Product_ID.index(selectionlist_ID[h])] - Product_Cost[Product_ID.index(selectionlist_ID[h])]) * Product_Product_sales[Product_ID.index(selectionlist_ID[h])]) # - (setup_cost + replenishment_cost))
                        #print("sel=", Product_Product_sales[Product_ID.index(selectionlist_ID[h])])
            # cargolane_empty.append(cargolane_occupied[h])
                   
        df = pd.DataFrame({"ID": sel_sort, "revenue": sel_sort_rev, "sales": sel_sort_sales})
        # print(sel_sort)
        # df.sort_values(by = ["sales", "ID"])
        df.sort_values(by = ["revenue"], ascending = False)
        df_sel_sort = df["ID"]
        selectionlist_sorted.append(df_sel_sort)
        # print(selectionlist_sorted)
    
    for i in range(len(selectionlist_sorted)):
        for j in range(len(selectionlist_sorted[i])):
            if selectionlist_sorted[i][j] == "zzzzzz":
                selectionlist_sorted[i][j] = ""
   
    # cargolane assignment
    quantity_displayed=[]#Sikr
    purchasing_cost=[]
    index0 = 0
    index1 = 0
    index2 = 0
    index3 = 0
    index4 = 0
    index5 = 0
    indexs1 = 0
    indexs2 = 0
    indexs3 = 0
    indexs4 = 0
    cargoID = 1
    
    for i in CargoLane_Type:
        if i == 0:
            selection_ID.append(selectionlist_sorted[0][index0])
            selection_price.append(0)
            selection_sales.append(0)
            selection_profit.append(0)
            selection_new.append(0)
            cargolane_empty.append(0)
            quantity_displayed.append(0)
            purchasing_cost.append(0)
            index0 += 1
            cargoID += 1 #####################################################
        elif i == 1:
            I = selectionlist_sorted[1][index1]
            # print("1",I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                quantity_displayed.append(0)
                purchasing_cost.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
            elif I[-1] == "_": # 最後一個為_代表推薦品項 # The last one is _ to represent the recommended item
                I = I[:-1]
                if I == "": # 避免有"_" 避免有"_"
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                else: # 代表推薦品項 # 代表推薦品項
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)])  * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else: # 原選取品項(不是推薦) ORIGINAL OPTIONS (NOT RECOMMENDED)
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) #- (setup_cost+replenishment_cost))#
                # selection_sales.append(copy_sales_1[ID_CargoLane1.index(I)])#
                # selection_profit.append(copy_profit_1[ID_CargoLane1.index(I)])#
            index1 += 1
            cargoID += 1 #####################################################
        elif i == 2:
            I = selectionlist_sorted[2][index2]
            # print("2",I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        # print(cargolane_empty)
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)])#- (setup_cost+replenishment_cost))#
                # selection_sales.append(copy_sales_2[ID_CargoLane2.index(I)])#
                # selection_profit.append(copy_profit_2[ID_CargoLane2.index(I)])#
            index2 += 1
            cargoID += 1 #####################################################
        elif i == 3:
            I = selectionlist_sorted[3][index3]
            # print("3", I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)])  * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                # selection_sales.append(copy_sales_3[ID_CargoLane3.index(I)])#
                # selection_profit.append(copy_profit_3[ID_CargoLane3.index(I)])#
            index3 += 1
            cargoID += 1 #####################################################
        elif i == 4:
            I = selectionlist_sorted[4][index4]
            # print("4", I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append()
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                # selection_sales.append(copy_sales_4[ID_CargoLane4.index(I)])#
                # selection_profit.append(copy_profit_4[ID_CargoLane4.index(I)])#
            index4 += 1
            cargoID += 1 #####################################################
        elif i == 5:
            I = selectionlist_sorted[5][index5]
            # print("5", I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                # selection_sales.append(copy_sales_5[ID_CargoLane5.index(I)])#
                # selection_profit.append(copy_profit_5[ID_CargoLane5.index(I)])#
            index5 += 1
            cargoID += 1 #####################################################
        elif i == "s1.0" or i == "s1":
            I = selectionlist_sorted[6][indexs1]
            # print("s1", I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                # selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                # selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)])#
            indexs1 += 1
            cargoID += 1 #####################################################
        elif i == "s2.0" or i == "s2":
            I = selectionlist_sorted[7][indexs2]
            # print("s2", I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)])  * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)])  * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) #- (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                # selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                # selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)])#
            indexs2 += 1
            cargoID += 1 #####################################################
        elif i == "s3.0" or i == "s3":
            I = selectionlist_sorted[8][indexs3]
            # print("s3",I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                # selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                # selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)])#
            indexs3 += 1
            cargoID += 1 #####################################################
        elif i == "s4.0" or i == "s4":
            I = selectionlist_sorted[9][indexs4]
            # print("s4", I)
            if I == "":
                selection_ID.append("empty")
                selection_price.append(0)
                selection_sales.append(0)
                selection_profit.append(0)
                selection_new.append(0)
                cargolane_empty.append(CargoLane_ID[cargoID - 1])
                quantity_displayed.append(0)
                purchasing_cost.append(0)
            elif I[-1] == "_":
                I = I[:-1]
                if I == "":
                    selection_ID.append("empty")
                    selection_price.append(0)
                    selection_sales.append(0)
                    selection_profit.append(0)
                    selection_new.append(0)
                    cargolane_empty.append(CargoLane_ID[cargoID - 1])
                    quantity_displayed.append(0)
                    purchasing_cost.append(0)
                else:
                    if mode == str(2):
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)])  * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                    else:
                        cargolane_empty.append(CargoLane_ID[cargoID - 1])
                        selection_ID.append(I)
                        selection_price.append(Product_Price[Product_ID.index(I)])
                        selection_new.append(Product_New[Product_ID.index(I)])
                        selection_sales.append(Product_Product_sales[Product_ID.index(I)] * recommended_profit_ratio)#
                        selection_profit.append(((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)])  * recommended_profit_ratio)
                        quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                        purchasing_cost.append(Product_Cost[Product_ID.index(I)])
            else:
                cargolane_empty.append(0)
                selection_ID.append(I)
                selection_price.append(Product_Price[Product_ID.index(I)])
                selection_new.append(Product_New[Product_ID.index(I)])
                quantity_displayed.append(round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(I)]))
                purchasing_cost.append(Product_Cost[Product_ID.index(I)])
                if I in Demand_Product_ID:
                    selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)]) # - (setup_cost+replenishment_cost))#
                else:
                    selection_sales.append(Product_Product_sales[Product_ID.index(I)])#
                    selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Product_Product_sales[Product_ID.index(I)]) #- (setup_cost+replenishment_cost))#
                # selection_sales.append(Demand_Product_Sales[Demand_Product_ID.index(I)])#
                # selection_profit.append((Product_Price[Product_ID.index(I)] - Product_Cost[Product_ID.index(I)]) * Demand_Product_Sales[Demand_Product_ID.index(I)])#
            indexs4 += 1
            cargoID += 1 #####################################################
        
        cargolane_empty = list(set(cargolane_empty))
        cargolane_empty.sort()
        cargolane_empty_list = cargolane_empty[1:]
        recommend_list = []
        
        for i in cargolane_empty_list:
            # recommend_list.append(selection_ID[i-1])
            recommend_list.append(selection_ID[CargoLane_ID.index(i)])
            
        # for k in range(len(selection_sales)):
        #     if selection_ID[k] in Demand_zero and k+1 not in cargolane_empty_list:
        #         selection_sales[k] = 0
        #         selection_profit[k] = 0
        
        selection_empty = []
        for i in range(len(selection_ID)):
            if CargoLane_ID[i] in cargolane_empty_list:
                selection_empty.append(1)
            else:
                selection_empty.append(0)
                
    # print(selection_ID)  
    # print("##")       
    # print("Profit1=",selection_profit)  
    # # print("##")
    # print("QTY=", quantity_displayed)
    # print("Sales before=",selection_sales)
    # print("Profit before=",selection_profit)
    
    # print("******")
    # print("Purch=",purchasing_cost)
    
    ### Updating the objective value
    cross_matrix=[]
    sjmn=[]
    random.seed()
    
    for i in selection_ID:
        cross_elasticity=[]
        random.seed()
        for i in range(len(selection_ID)):
            rando = random.uniform(-0.05,0.05)
            rando=round(rando,3)
            cross_elasticity.append(rando)
        cross_matrix.append(cross_elasticity)
        
    for i in range(len(selection_ID)):
        cross_matrix[i][i]=0.0
    # print("crossmatrix", cross_matrix)
    
    capacity_arr=[]
    for i in range(len(selection_ID)):
        capacity_arr.append(quantity_displayed)
    sjm_matrix= np.power(capacity_arr,cross_matrix)
    # print("sjm_matrix", sjm_matrix)
    
    for i in range(len(sjm_matrix)):
        f=np.prod(sjm_matrix[i])
        sjmn.append(f)
        
    # print(sjmn)
    # Define parameters
    # alpha = 2.5
    # sikr = 10

    mean = 0  # Mean of the normal distribution
    std = 1 # Standard deviation of the normal distribution
    # Generate stochastic demand values
    experror = []
    for _ in range(len(selection_ID)):
        error = random.normalvariate(mean, std)  # Generate random error term
        error1 = math.exp(error)
        experror.append(error1)
    # print("experror", experror)


    # Print demand values
    # for i, demand in enumerate(demand_values):
    #     print(f"Iteration {i + 1}: Demand = {demand}")
    

    alpha= random.uniform(5,10)
    space_elas= random.uniform(0.2,0.4)
    cross_elas= random.uniform(-0.05,0.05)
    problostsales=0.1
    inventory_cost=[]
    backroom_cost=[]
    display_cost=[]
    ordering_cost=[]
    replenishment=[]
    stockout=[]
    lostsales=[]
    # error=[]
    # epsilon=[]
    
    for i in range(len(selection_ID)): #!!!!!
        selection_sales[i]= round(max((alpha * (quantity_displayed[i]**space_elas)*(sjmn[i])* experror[i]),1)) #Dikr
        # print("selection_sales",selection_sales)
        replenishment.append(round(max(math.sqrt(unit_ordering_cost[Product_ID.index(selection_ID[i])] / (((unit_inventory_cost[Product_ID.index(selection_ID[i])]/2) + unit_backroom_cost[Product_ID.index(selection_ID[i])]) * selection_sales[i])),1)))
        # print("ordering cost", unit_ordering_cost[Product_ID.index(selection_ID[i])])
        # print("inventory cost",unit_inventory_cost[Product_ID.index(selection_ID[i])])
        # print("backroom cost",unit_backroom_cost[Product_ID.index(selection_ID[i])])
        # print("demand ", selection_sales[i])
        # print("replenishment",replenishment)
        stockout.append(round(max(selection_sales[i]-quantity_displayed[i],0)))
        lostsales.append(max((Product_Price[Product_ID.index(selection_ID[i])]-Product_Cost[Product_ID.index(selection_ID[i])])*(selection_sales[i]*replenishment[i]-quantity_displayed[i]),0))
        inventory_cost.append(unit_inventory_cost[Product_ID.index(selection_ID[i])]*(quantity_displayed[i]+(selection_sales[i]*replenishment[i]/2)))
        backroom_cost.append(unit_backroom_cost[Product_ID.index(selection_ID[i])]*selection_sales[i]*replenishment[i])
        display_cost.append(unit_display_cost[Product_ID.index(selection_ID[i])]* quantity_displayed[i] * replenishment[i])
        ordering_cost.append(unit_ordering_cost[Product_ID.index(selection_ID[i])]/ replenishment[i])
        selection_profit[i]=((Product_Price[Product_ID.index(selection_ID[i])]-Product_Cost[Product_ID.index(selection_ID[i])])*selection_sales[i]* replenishment[i]) - inventory_cost[i] - backroom_cost[i]- display_cost[i]- ordering_cost[i] - lostsales[i]
    
    # for i, demand in enumerate(error):
    #     print(f"Iteration {i + 1}: Demand = {demand}")
    # print("error =", error)
    # print("ID=", selection_ID)
    # print("sales after=", selection_sales)
    # print("stockout=", stockout)
    # print("lost sales=", lostsales)
    # print("ic=", inventory_cost)
    # print("bc=",backroom_cost)
    # print("dc=", display_cost)
    # print("oc=", ordering_cost)
    # print("replenishment", replenishment)
    # print("Profit After=",selection_profit)
    # print("**********************************")
    
    return selection_ID, selection_price, selection_sales, selection_profit, selection_new, cargolane_empty_list, recommend_list, selection_empty, inventory_cost,backroom_cost,display_cost,ordering_cost, purchasing_cost, replenishment, stockout, lostsales, quantity_displayed

#%%
# GA population
def initial_solution(chro_num, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, Current_Product, Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, mode , setup_cost, replenishment_cost):
    Pro_chro = []
    Pro_chro_price = []
    Pro_chro_sales = []
    Pro_chro_profit = []
    Pro_chro_new = []
    Pro_chro_cargolane_occupied = []
    Pro_chro_recommend_prod = []
    Pro_chro_cargolane_occupied_list = []
    Pro_chro_inventory_cost=[]
    Pro_chro_backroom_cost=[]
    Pro_chro_display_cost=[]
    Pro_chro_ordering_cost=[]
    Pro_chro_purchasing_cost=[]
    Pro_chro_replenishment=[]
    Pro_chro_stockout=[]
    Pro_chro_lostsales=[]
    Pro_chro_quantity_display=[]
    
    # to make heuristic solution be same in every time
    selection_ini_, selection_price_ini_, selection_sales_ini_, selection_profit_ini_, selection_new_ini_, cargolane_occupied_ini_, recommended_prod_ini_, cargolane_occupiedlist_ini_, inventory_cost_ini_,backroom_cost_ini_,display_cost_ini_,ordering_cost_ini_, purchasing_cost_ini_, replenishment_ini_, stockout_ini_, lostsales_ini_, quantity_display_ini_ = chomosome(ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, cargolane_type_num, Product_New, Product_ID, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, Cost_CargoLane1, Cost_CargoLane2, Cost_CargoLane3, Cost_CargoLane4, Cost_CargoLane5, Recommend_cost1, Recommend_cost2, Recommend_cost3, Recommend_cost4, Recommend_cost5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, "max", Product_Product_sales, setup_cost, replenishment_cost,CargoLane_Diameter_Max_1,Product_Length, unit_inventory_cost,unit_backroom_cost,unit_display_cost,unit_ordering_cost, Product_Cost)
    Pro_chro.append(selection_ini_)
    Pro_chro_price.append(selection_price_ini_)
    Pro_chro_sales.append(selection_sales_ini_)
    Pro_chro_profit.append(selection_profit_ini_)
    Pro_chro_new.append(selection_new_ini_)
    Pro_chro_cargolane_occupied.append(cargolane_occupied_ini_)
    Pro_chro_recommend_prod.append(recommended_prod_ini_)
    Pro_chro_cargolane_occupied_list.append(cargolane_occupiedlist_ini_)
    Pro_chro_inventory_cost.append(inventory_cost_ini_)
    Pro_chro_backroom_cost.append(backroom_cost_ini_)
    Pro_chro_display_cost.append(display_cost_ini_)
    Pro_chro_ordering_cost.append(ordering_cost_ini_)
    Pro_chro_purchasing_cost.append(purchasing_cost_ini_)
    Pro_chro_replenishment.append(replenishment_ini_)
    Pro_chro_stockout.append(stockout_ini_)
    Pro_chro_lostsales.append(lostsales_ini_)
    Pro_chro_quantity_display.append(quantity_display_ini_)
    
    
    if mode == str(1):
        for k in range(chro_num-1):
            selection_ini, selection_price_ini, selection_sales_ini, selection_profit_ini, selection_new_ini, cargolane_occupied_ini, recommended_prod_ini, cargolane_occupiedlist_ini, inventory_cost_ini ,backroom_cost_ini ,display_cost_ini ,ordering_cost_ini, purchasing_cost_ini, replenishment_ini, stockout_ini, lostsales_ini, quantity_display_ini = chomosome(ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, cargolane_type_num, Product_New, Product_ID, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, Cost_CargoLane1, Cost_CargoLane2, Cost_CargoLane3, Cost_CargoLane4, Cost_CargoLane5, Recommend_cost1, Recommend_cost2, Recommend_cost3, Recommend_cost4, Recommend_cost5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, "random", Product_Product_sales, setup_cost, replenishment_cost, CargoLane_Diameter_Max_1,Product_Length,unit_inventory_cost,unit_backroom_cost,unit_display_cost,unit_ordering_cost, Product_Cost)
            Pro_chro.append(selection_ini)
            Pro_chro_price.append(selection_price_ini)
            Pro_chro_sales.append(selection_sales_ini)
            Pro_chro_profit.append(selection_profit_ini)
            Pro_chro_new.append(selection_new_ini)
            Pro_chro_cargolane_occupied.append(cargolane_occupied_ini)
            Pro_chro_recommend_prod.append(recommended_prod_ini)
            Pro_chro_cargolane_occupied_list.append(cargolane_occupiedlist_ini)
            Pro_chro_inventory_cost.append(inventory_cost_ini)
            Pro_chro_backroom_cost.append(backroom_cost_ini)
            Pro_chro_display_cost.append(display_cost_ini)
            Pro_chro_ordering_cost.append(ordering_cost_ini)
            Pro_chro_purchasing_cost.append(purchasing_cost_ini)
            Pro_chro_replenishment.append(replenishment_ini)
            Pro_chro_stockout.append(stockout_ini)
            Pro_chro_lostsales.append(lostsales_ini)
            Pro_chro_quantity_display.append(quantity_display_ini)
    else:
        for k in range(chro_num-1):
            selection_ini, selection_price_ini, selection_sales_ini, selection_profit_ini, selection_new_ini, cargolane_occupied_ini, recommended_prod_ini, cargolane_occupiedlist_ini, inventory_cost_ini ,backroom_cost_ini ,display_cost_ini ,ordering_cost_ini, purchasing_cost_ini, replenishment_ini, stockout_ini, lostsales_ini, quantity_display_ini = chomosome(ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, cargolane_type_num, Product_New, Product_ID, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, Cost_CargoLane1, Cost_CargoLane2, Cost_CargoLane3, Cost_CargoLane4, Cost_CargoLane5, Recommend_cost1, Recommend_cost2, Recommend_cost3, Recommend_cost4, Recommend_cost5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, "random", Product_Product_sales, setup_cost, replenishment_cost, CargoLane_Diameter_Max_1,Product_Length, unit_inventory_cost,unit_backroom_cost,unit_display_cost,unit_ordering_cost, Product_Cost)
            Pro_chro.append(selection_ini)
            Pro_chro_price.append(selection_price_ini)
            Pro_chro_sales.append(selection_sales_ini)
            Pro_chro_profit.append(selection_profit_ini)
            Pro_chro_new.append(selection_new_ini)
            Pro_chro_cargolane_occupied.append(cargolane_occupied_ini)
            Pro_chro_recommend_prod.append(recommended_prod_ini)
            Pro_chro_cargolane_occupied_list.append(cargolane_occupiedlist_ini)
            Pro_chro_inventory_cost.append(inventory_cost_ini)
            Pro_chro_backroom_cost.append(backroom_cost_ini)
            Pro_chro_display_cost.append(display_cost_ini)
            Pro_chro_ordering_cost.append(ordering_cost_ini)
            Pro_chro_purchasing_cost.append(purchasing_cost_ini)
            Pro_chro_replenishment.append(replenishment_ini)
            Pro_chro_stockout.append(stockout_ini)
            Pro_chro_lostsales.append(lostsales_ini)
            Pro_chro_quantity_display.append(quantity_display_ini)
            # print(len(Pro_chro[-1]))

    #　save the current solution
    # if mode != str(1):
    #     Current_ID, Current_price, Current_sales, Current_profit, Current_New, Current_occupied, Current_recommended, Current_occupiedlist = current_info(Current_Product, Product_ID, Demand_Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, Product_Cost, setup_cost, replenishment_cost)
    #     Pro_chro.append(Current_ID)
    #     Pro_chro_price.append(Current_price)
    #     Pro_chro_sales.append(Current_sales)
    #     Pro_chro_profit.append(Current_profit)
    #     Pro_chro_new.append(Current_New)
    #     Pro_chro_cargolane_occupied.append(Current_occupied)
    #     Pro_chro_recommend_prod.append(Current_recommended)
    #     Pro_chro_cargolane_occupied_list.append(Current_occupiedlist)
    # print("")
    # print(Pro_chro)
    # # print("")
    # print("Pro_chro_profit=", Pro_chro_profit)
    return Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, Pro_chro_cargolane_occupied_list, Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display

#%%
# check the constraints
def check(chro_ID, chro_new, cargotype, prodtype, num, new_prod_ratio, chro_price, chro_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, chro_recommend, Product_New, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display):
    copy_chro = chro_ID.copy()
    check_type_list = 0
    check_new_list = 0
    check_prod_cargolane_num = 0
    atleast = math.ceil(len(chro_ID) * (new_prod_ratio / 100))
    
    for i in range(len(chro_ID)):
        check_new_list += chro_new[i]
        if chro_ID[i] in ["", "empty"]:
            typeofprod = 0
            pass
        else:
            typeofprod = Product_Type[Product_ID.index(chro_ID[i])]
            
        # if i in list(locate(cargotype, lambda x: x == 0)):
        #     pass
        # elif typeofprod == 1 and (cargotype[i] not in [1, 2]):
        #     check_type_list += 1
        # elif typeofprod == 2 and (cargotype[i] not in [2]):
        #     check_type_list += 1
        # elif typeofprod == 3 and (cargotype[i] not in [3, 4, 5]):
        #     check_type_list += 1
        # elif typeofprod == 4 and (cargotype[i] not in [4, 5]):
        #     check_type_list += 1
        # elif typeofprod == 5 and (cargotype[i] not in [4, 5]):
        #     check_type_list += 1
    
    # to check the min selected product > len of product demand
    except_recommended = []
    # for i in range(len(copy_chro)):
    #     if i+1 in chro_occupied:
    #         pass
    #     else:
    #         except_recommended.append(copy_chro[i])
    for i in range(len(copy_chro)):
        if CargoLane_ID[i] in chro_occupied:
            pass
        else:
            except_recommended.append(copy_chro[i])
    
    while "" in except_recommended:
        except_recommended.remove("")
    while 0 in except_recommended:
        except_recommended.remove(0)
    while "empty" in except_recommended:
        except_recommended.remove("empty")
    
    for i in range(len(except_recommended)):
        if except_recommended[i] not in Demand_Product_ID:
            pass
        elif except_recommended.count(except_recommended[i]) > Product_max_cargolanenum[Demand_Product_ID.index(except_recommended[i])]:
            check_prod_cargolane_num += 1
    
    con_prod_num = len(list(set(except_recommended))) >= num # 檢查選取商品數是否符合最小商品需求數; # Check whether the number of selected items meets the minimum required number of items
    con_type = check_type_list == 0 # 檢查商品類別是否符合貨道類別限制 # Check if the commodity category meets the cargo lane category restrictions
    con_new = check_new_list >= atleast # 檢查新品數是否符合最小新品需求 # Check whether the number of new products meets the minimum new product requirements
    # con_prod_cargolane_num = check_prod_cargolane_num <= 0 # 檢查商品貨道數是否符合該品項最大擺放貨道數 # Check whether the number of commodity lanes meets the maximum number of lanes for this item
    
    
    # calculate opportunity loss 
    # product_total_capacity = [0] * len(Demand_Product_ID)
    # require_not_enough_penalty = 0
    # for i in range(len(Demand_Product_ID)): # occupied 也要排除掉
    #     for j in range(len(chro_ID)):
    #         if CargoLane_ID[j] in chro_occupied:
    #             pass
    #         elif Demand_Product_ID[i] == chro_ID[j]:
    #             product_total_capacity[i] += CargoLane_Capacity[j]
    #             #print(j)
    #             #print(product_total_capacity)
    
    # Replenishment_times = (30 / CargoLane_Average_Replenishment[0])
    # for i in range(len(product_total_capacity)):
    #     if replenishment_per_time[i] > product_total_capacity[i]:
    #         require_not_enough_penalty += abs(replenishment_per_time[i] - product_total_capacity[i]) * Replenishment_times * Product_Price[Product_ID.index(Demand_Product_ID[i])]
    #         print(require_not_enough_penalty)
            
    # check the times of recommend product <= 2
    check_recommend = 0
    copy_recommend = chro_recommend.copy()
    copy_recommend_list = list(OrderedDict.fromkeys(copy_recommend))
    
    while "empty" in copy_recommend:
        copy_recommend.remove("empty")
    
    for i in copy_recommend_list:
        if copy_recommend.count(i) > 2:
            check_recommend += 1
    
    con_recommend_num = check_recommend == 0
    
    if mode == str(1):
        if list(set(Product_New)) == [0]:
            if con_type == False or con_prod_num == False: # or con_prod_cargolane_num == False:
                constraintornot = False
            else:
                constraintornot = True
        else:
            if con_type == False or con_new == False or con_prod_num == False: # or con_prod_cargolane_num == False:
                constraintornot = False
            else:
                constraintornot = True
    else:
        if list(set(Product_New)) == [0]:
            if con_type == False or con_prod_num == False or con_recommend_num == False: # 測試新品限制式
                constraintornot = False
            else:
                constraintornot = True
        else:
            if con_type == False or con_new == False or con_prod_num == False or con_recommend_num == False:
                constraintornot = False
            else:
                constraintornot = True
                
    # print(con_type, con_prod_num, con_recommend_num)
    # print(constraintornot)
        
    return constraintornot
#require_not_enough_penalty
    
#%%
# GA objective(fitness)
def objective(chro_profit, chro_ID, chro_new, cargotype, prodtype, num, new_prod_ratio, chro_price, chro_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, chro_recommend, Product_New, chro_cargolane_occupied_list, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display):
    each_chro_profit = []                                                      # 紀錄每個貨道的利潤
    #oppo_loss_list = []
    #each_chro_profit_withloss = []
    # copy_chro_recommend = chro_recommend.copy()
    cc_chro_ID = copy.deepcopy(chro_ID)
    cc_chro_profit = copy.deepcopy(chro_profit)

    for i in range(len(chro_ID)):
        # profit_matrix = pd.DataFrame({"ID": chro_ID[i], "Profit": chro_profit[i], "Empty": chro_cargolane_occupied_list[i]})
        # profit_matrix_without_duplicates = profit_matrix.drop_duplicates(subset = ["ID", "Profit", "Empty"])
        for k in range(len(chro_ID[i])):
            if CargoLane_ID[k] in chro_occupied[i]:
                cc_chro_ID[i][CargoLane_ID.index(CargoLane_ID[k])] = 0
                cc_chro_profit[i][CargoLane_ID.index(CargoLane_ID[k])] = 0
        
        profit_matrix = pd.DataFrame({"ID": cc_chro_ID[i], "Profit": cc_chro_profit[i]})
        profit_matrix_without_duplicates = profit_matrix.drop_duplicates(subset = ["ID", "Profit"]) # !!!!!
        #each_chro_profit.append(sum(profit_matrix_without_duplicates["Profit"]))
        each_chro_profit.append(sum(profit_matrix["Profit"]))
        
        # for j in list(set(chro_recommend[i])):
        #     if chro_recommend[i].count(j) == 2:
        #         each_chro_profit[i] += chro_profit[i][CargoLane_ID.index((chro_occupied[i][chro_recommend[i].index(j)]))]

        for g in range(len(chro_occupied[i])):
            each_chro_profit[i] += chro_profit[i][CargoLane_ID.index(chro_occupied[i][g])]

    # for j in range(len(chro_profit)):
    #     meetornot = check(chro_ID[j], chro_new[j], cargotype, prodtype, num, new_prod_ratio, chro_price[j], chro_occupied[j], replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, chro_recommend[j], Product_New, chro_inventory_cost[j], chro_backroom_cost[j], chro_display_cost[j], chro_ordering_cost[j], chro_purchasing_cost[j], chro_replenishment[j], chro_stockout[j], chro_lostsales[j])

        #meetornot, oppo_loss = check(chro_ID[j], chro_new[j], cargotype, prodtype, num, new_prod_ratio, chro_price[j], chro_occupied[j], replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, chro_recommend[j], Product_New)
        #oppo_loss_list.append(oppo_loss)
        #each_chro_profit_withloss.append(each_chro_profit[j] - oppo_loss)
        # if meetornot == False:
        #    each_chro_profit[j] = 0.000000000001
           #each_chro_profit_withloss[j] = 0.000000000001
            
    return each_chro_profit
#oppo_loss_list, each_chro_profit_withloss

#%%
# test fitness def
# sku_min_num = len(list(set(Demand_Product_ID)))
# Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, Pro_chro_cargolane_occupied_list = initial_solution(12, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, Current_Product, Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4)
# each_chro_profit, oppo_loss_list, each_chro_profit_withloss = objective(Pro_chro_profit, Pro_chro, Pro_chro_new, CargoLane_Type, Product_Type, sku_min_num, new_prod_ratio, Pro_chro_price, Pro_chro_cargolane_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, Pro_chro_recommend_prod, Product_New, Pro_chro_cargolane_occupied_list)
# aa = 7
# meetornot, oppo_loss = check(Pro_chro[aa], Pro_chro_new[aa], CargoLane_Type, Product_Type, sku_min_num, new_prod_ratio, Pro_chro_price, Pro_chro_cargolane_occupied[aa], replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, Pro_chro_recommend_prod[aa], Product_New)

# except_recommended = []
# for i in range(len(Pro_chro[aa])):
#     if i+1 in Pro_chro_cargolane_occupied[aa]:
#         pass
#     else:
#         except_recommended.append(Pro_chro[aa][i])
    
# while "" in except_recommended:
#     except_recommended.remove("")
# while str() in except_recommended:
#     except_recommended.remove(str())   
# while 0 in except_recommended:
#     except_recommended.remove(0)
# while "empty" in except_recommended:
#     except_recommended.remove("empty")
# # while np.nan in except_recommended:
# #     except_recommended.remove(np.nan)
    
# a = list(set(except_recommended))

# con_prod_num = len(list(set(except_recommended))) >= sku_min_num
# print(con_prod_num)

# check_prod_cargolane_num = 0
# for i in Pro_chro[1]:
#     if i not in Demand_Product_ID:
#         pass
#     elif Pro_chro.count(i) > Product_max_cargolanenum[Demand_Product_ID.index(i)]:
#         check_prod_cargolane_num += 1
            
#%%
# # definition for oppotunity loss 
# def oppoloss(Demand_Product_ID, chro_ID, chro_occupied):
#     # 計算oppotunity loss 
#     product_total_capacity = [0] * len(Demand_Product_ID)
#     require_not_enough_penalty = 0
#     for i in range(len(Demand_Product_ID)): # occupied 也要排除掉
#         for j in range(len(chro_ID)):
#             if CargoLane_ID[j] in chro_occupied:
#                 pass
#             elif Demand_Product_ID[i] == chro_ID[j]:
#                 product_total_capacity[i] += CargoLane_Capacity[j]
    
#     Replenishment_times = (30 / CargoLane_Average_Replenishment[0])
#     for i in range(len(product_total_capacity)):
#         if replenishment_per_time[i] > product_total_capacity[i]:
#             require_not_enough_penalty += abs(replenishment_per_time[i] - product_total_capacity[i]) * Replenishment_times * Product_Price[Product_ID.index(Demand_Product_ID[i])]
    
#     return require_not_enough_penalty

#%%
# GA selection: max & roulette
#def selection(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, each_chro_profit, oppo_loss_list):
def selection(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod,chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit):
    temp_chro = copy.deepcopy(chro)
    temp_each_chro_profit = copy.deepcopy(each_chro_profit)
    #temp_oppo_loss_list = copy.deepcopy(oppo_loss_list)
  
    # for i in range(len(each_chro_profit)):
    #     temp_each_chro_profit[i] += temp_oppo_loss_list[i]
    
    max_profit = max(temp_each_chro_profit)
    max_index = temp_each_chro_profit.index(max_profit)
    
    del temp_chro[max_index]
    del temp_each_chro_profit[max_index]    
    
    rou = np.random.rand(1)
    
    profit_sum = sum(temp_each_chro_profit)
    each_chro_profit_prob = []
    for i in range(len(temp_each_chro_profit)):        
        each_chro_profit_prob.append(temp_each_chro_profit[i] / profit_sum)

    for i in range(len(each_chro_profit_prob)):
        if sum(each_chro_profit_prob[:i]) < rou <= sum(each_chro_profit_prob[:i+1]):
            if i >= max_index:
                sec_choosen_chro = chro[i+1]
                sec_choosen_price = chro_price[i+1]
                sec_choosen_sales = chro_sales[i+1]
                sec_choosen_profit = chro_profit[i+1]
                sec_choosen_new = chro_new[i+1]
                sec_choosen_occupied = chro_cargolane_occupied[i+1]
                sec_choosen_recommend = chro_recommend_prod[i+1]
                sec_choosen_inventory_cost= chro_inventory_cost[i+1]
                sec_choosen_backroom_cost= chro_backroom_cost[i+1]
                sec_choosen_display_cost= chro_display_cost[i+1]
                sec_choosen_ordering_cost= chro_ordering_cost[i+1]
                sec_choosen_purchasing_cost= chro_purchasing_cost[i+1]
                sec_choosen_replenishment = chro_replenishment[i+1]
                sec_choosen_stockout = chro_stockout[i+1]
                sec_choosen_lostsales= chro_lostsales[i+1]
                sec_choosen_quantity_display = chro_quantity_display[i+1]
                sec_index = i+1
                break
            else:
                sec_choosen_chro = chro[i]
                sec_choosen_price = chro_price[i]
                sec_choosen_sales = chro_sales[i]
                sec_choosen_profit = chro_profit[i]
                sec_choosen_new = chro_new[i]
                sec_choosen_occupied = chro_cargolane_occupied[i]
                sec_choosen_recommend = chro_recommend_prod[i]
                sec_choosen_inventory_cost= chro_inventory_cost[i]
                sec_choosen_backroom_cost= chro_backroom_cost[i]
                sec_choosen_display_cost= chro_display_cost[i]
                sec_choosen_ordering_cost= chro_ordering_cost[i]
                sec_choosen_purchasing_cost= chro_purchasing_cost[i]
                sec_choosen_replenishment= chro_replenishment[i]
                sec_choosen_stockout = chro_stockout[i]
                sec_choosen_lostsales= chro_lostsales[i]
                sec_choosen_quantity_display = chro_quantity_display[i]
                sec_index = i
                break
    
    return chro[max_index], chro_price[max_index], chro_sales[max_index], chro_profit[max_index], chro_new[max_index], chro_cargolane_occupied[max_index], chro_recommend_prod[max_index],chro_inventory_cost[max_index], chro_backroom_cost[max_index], chro_display_cost[max_index], chro_ordering_cost[max_index], chro_purchasing_cost[max_index], chro_replenishment[max_index], chro_stockout[max_index], chro_lostsales[max_index], chro_quantity_display[max_index],\
        sec_choosen_chro, sec_choosen_price, sec_choosen_sales, sec_choosen_profit, sec_choosen_new, sec_choosen_occupied, sec_choosen_recommend,sec_choosen_inventory_cost, sec_choosen_backroom_cost,sec_choosen_display_cost,sec_choosen_ordering_cost,sec_choosen_purchasing_cost,sec_choosen_replenishment, sec_choosen_stockout, sec_choosen_lostsales, sec_choosen_quantity_display, max_index, sec_index

#%%
# GA selection: max & roulette
#def selection_pure_rou(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, each_chro_profit, oppo_loss_list):
def selection_pure_rou(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod,chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display,each_chro_profit):

    # temp_chro = copy.deepcopy(chro)
    temp_each_chro_profit = copy.deepcopy(each_chro_profit)
    #temp_oppo_loss_list = copy.deepcopy(oppo_loss_list)
    
    # for i in range(len(temp_each_chro_profit)):
    #     temp_each_chro_profit[i] += temp_oppo_loss_list[i]
    
    profit_sum_first = sum(temp_each_chro_profit)
    each_chro_profit_prob_first = []
    for i in range(len(temp_each_chro_profit)):        
        each_chro_profit_prob_first.append(temp_each_chro_profit[i] / profit_sum_first)

    rou_first = np.random.rand(1)

    for i in range(len(each_chro_profit_prob_first)):
        if sum(each_chro_profit_prob_first[:i]) < rou_first <= sum(each_chro_profit_prob_first[:i+1]):
            # fir_choosen_chro = chro[i]
            # fir_choosen_price = chro_price[i]
            # fir_choosen_sales = chro_sales[i]
            # fir_choosen_profit = chro_profit[i]
            # fir_choosen_new = chro_new[i]
            # fir_choosen_occupied = chro_cargolane_occupied[i]
            # fir_choosen_recommend = chro_recommend_prod[i]
            fir_index = i
            break
    
    # fir_profit = temp_each_chro_profit[fir_index]
    
    # del temp_chro[fir_index]
    # del temp_each_chro_profit[fir_index]    
    
    rou = np.random.rand(1)
    
    profit_sum = sum(temp_each_chro_profit)
    each_chro_profit_prob = []
    for i in range(len(temp_each_chro_profit)):        
        each_chro_profit_prob.append(temp_each_chro_profit[i] / profit_sum)

    for i in range(len(each_chro_profit_prob)):
        if sum(each_chro_profit_prob[:i]) < rou <= sum(each_chro_profit_prob[:i+1]):
            sec_choosen_chro = chro[i]
            sec_choosen_price = chro_price[i]
            sec_choosen_sales = chro_sales[i]
            sec_choosen_profit = chro_profit[i]
            sec_choosen_new = chro_new[i]
            sec_choosen_occupied = chro_cargolane_occupied[i]
            sec_choosen_recommend = chro_recommend_prod[i]
            sec_choosen_inventory_cost= chro_inventory_cost[i]
            sec_choosen_backroom_cost= chro_backroom_cost[i]
            sec_choosen_display_cost= chro_display_cost[i]
            sec_choosen_ordering_cost= chro_ordering_cost[i]
            sec_choosen_purchasing_cost= chro_purchasing_cost[i]
            sec_choosen_replenishment= chro_replenishment[i]
            sec_choosen_stockout= chro_stockout[i]
            sec_choosen_lostsales= chro_lostsales[i]
            sec_choosen_quantity_display= chro_quantity_display[i]
            sec_index = i
            break
            # if i >= fir_index:
            #     sec_choosen_chro = chro[i+1]
            #     sec_choosen_price = chro_price[i+1]
            #     sec_choosen_sales = chro_sales[i+1]
            #     sec_choosen_profit = chro_profit[i+1]
            #     sec_choosen_new = chro_new[i+1]
            #     sec_choosen_occupied = chro_cargolane_occupied[i+1]
            #     sec_choosen_recommend = chro_recommend_prod[i+1]
            #     sec_index = i+1
            #     break
            # else:
            #     sec_choosen_chro = chro[i]
            #     sec_choosen_price = chro_price[i]
            #     sec_choosen_sales = chro_sales[i]
            #     sec_choosen_profit = chro_profit[i]
            #     sec_choosen_new = chro_new[i]
            #     sec_choosen_occupied = chro_cargolane_occupied[i]
            #     sec_choosen_recommend = chro_recommend_prod[i]
            #     sec_index = i
            #     break
    
    return chro[fir_index], chro_price[fir_index], chro_sales[fir_index], chro_profit[fir_index], chro_new[fir_index], chro_cargolane_occupied[fir_index], chro_recommend_prod[fir_index],chro_inventory_cost[fir_index], chro_backroom_cost[fir_index], chro_display_cost[fir_index], chro_ordering_cost[fir_index], chro_purchasing_cost[fir_index], chro_replenishment[fir_index], chro_stockout[fir_index], chro_lostsales[fir_index], chro_quantity_display[fir_index],\
        sec_choosen_chro, sec_choosen_price, sec_choosen_sales, sec_choosen_profit, sec_choosen_new, sec_choosen_occupied, sec_choosen_recommend, sec_choosen_inventory_cost, sec_choosen_backroom_cost,sec_choosen_display_cost,sec_choosen_ordering_cost,sec_choosen_purchasing_cost, sec_choosen_replenishment, sec_choosen_stockout, sec_choosen_lostsales, sec_choosen_quantity_display, fir_index, sec_index

#%%
# GA crossover
#def crossover(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, each_chro_profit_withloss):
def crossover(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod,chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost,selection1_ordering_cost, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new,selection2_inventory_cost, selection2_backroom_cost, selection2_display_cost,selection2_ordering_cost, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend):
    # cross_points = [np.random.randint(0, len(chro[0])-1)]
    # # cross_ran = random.random()    
    
    # copy_s1 = selection1.copy()
    # copy_profit_s1 = selection1_profit.copy()
    # copy_price_s1 = selection1_price.copy()
    # copy_sales_s1 = selection1_sales.copy()
    # copy_new_s1 = selection1_new.copy()
    # copy_occupied_s1 = selection1_occupied.copy()
    # copy_recommend_s1 = selection1_recommend.copy()
    
    # copy_s2 = selection2.copy()
    # copy_profit_s2 = selection2_profit.copy()
    # copy_price_s2 = selection2_price.copy()
    # copy_sales_s2 = selection2_sales.copy()
    # copy_new_s2 = selection2_new.copy()
    # copy_occupied_s2 = selection2_occupied.copy()
    # copy_recommend_s2 = selection2_recommend.copy()
    
    # temp_s1 = selection1.copy()
    # temp_profit_s1 = selection1_profit.copy()
    # temp_price_s1 = selection1_price.copy()
    # temp_sales_s1 = selection1_sales.copy()
    # temp_new_s1 = selection1_new.copy()
    # temp_occupied_s1 = selection1_occupied.copy()
    # temp_recommend_s1 = selection1_recommend.copy()
    
    # for cross in cross_points:
    #     s1isoccu = CargoLane_ID[cross] in copy_occupied_s1 # True = 該貨道是推薦品項 & cross為index, 所以要+1
    #     s2isoccu = CargoLane_ID[cross] in copy_occupied_s2
    #     # print(s1isoccu, s2isoccu) 
    #     if s1isoccu == True and s2isoccu == True: # 兩個都是推薦品項, 才換
    #         copy_s1[cross] = copy_s2[cross]
    #         copy_s2[cross] = temp_s1[cross]
    #         copy_profit_s1[cross] = copy_profit_s2[cross]
    #         copy_profit_s2[cross] = temp_profit_s1[cross]
    #         copy_price_s1[cross] = copy_price_s2[cross]
    #         copy_price_s2[cross] = temp_price_s1[cross]
    #         copy_sales_s1[cross] = copy_sales_s2[cross]
    #         copy_sales_s2[cross] = temp_sales_s1[cross]
    #         copy_new_s1[cross] = copy_new_s2[cross]
    #         copy_new_s2[cross] = temp_new_s1[cross]
    #         # print(len(copy_recommend_s1), len(copy_occupied_s1), len(copy_recommend_s2), len(copy_occupied_s2)) 
    #         copy_recommend_s1[copy_occupied_s1.index(CargoLane_ID[cross])] = copy_recommend_s2[copy_occupied_s2.index(CargoLane_ID[cross])]
    #         copy_recommend_s2[copy_occupied_s2.index(CargoLane_ID[cross])] = temp_recommend_s1[temp_occupied_s1.index(CargoLane_ID[cross])]
    #     elif s1isoccu == False and s2isoccu == False: # 兩個都不是推薦品項, 才換
    #         copy_s1[cross] = copy_s2[cross]
    #         copy_s2[cross] = temp_s1[cross]
    #         copy_profit_s1[cross] = copy_profit_s2[cross]
    #         copy_profit_s2[cross] = temp_profit_s1[cross]
    #         copy_price_s1[cross] = copy_price_s2[cross]
    #         copy_price_s2[cross] = temp_price_s1[cross]
    #         copy_sales_s1[cross] = copy_sales_s2[cross]
    #         copy_sales_s2[cross] = temp_sales_s1[cross]
    #         copy_new_s1[cross] = copy_new_s2[cross]
    #         copy_new_s2[cross] = temp_new_s1[cross]
    
    # # 如果只要相符就直接替換, 不管結果是否比較好
    
    # profit1_matrix = pd.DataFrame({"ID": copy_s1, "Profit": copy_profit_s1})
    # profit1_matrix_without_duplicates = profit1_matrix.drop_duplicates(subset = ["ID", "Profit"])
    # profit1 = (sum(profit1_matrix_without_duplicates["Profit"]))
    
    # profit2_matrix = pd.DataFrame({"ID": copy_s2, "Profit": copy_profit_s2})
    # profit2_matrix_without_duplicates = profit2_matrix.drop_duplicates(subset = ["ID", "Profit"])
    # profit2 = (sum(profit2_matrix_without_duplicates["Profit"]))
    
    # whichbigger = profit1 > profit2
    
    # if whichbigger == True: #profit1 bigger
    #     chro[max_index] = copy_s1
    #     chro_price[max_index] = copy_price_s1
    #     chro_sales[max_index] = copy_sales_s1
    #     chro_profit[max_index] = copy_profit_s1
    #     chro_new[max_index] = copy_new_s1
    #     chro_cargolane_occupied[max_index] = copy_occupied_s1
    #     chro_recommend_prod[max_index] = copy_recommend_s1
        
    #     chro[sec_index] = copy_s2
    #     chro_price[sec_index] = copy_price_s2
    #     chro_sales[sec_index] = copy_sales_s2
    #     chro_profit[sec_index] = copy_profit_s2
    #     chro_new[sec_index] = copy_new_s2
    #     chro_cargolane_occupied[sec_index] = copy_occupied_s2
    #     chro_recommend_prod[sec_index] = copy_recommend_s2
    # else: #profit2 bigger
    #     chro[max_index] = copy_s2
    #     chro_price[max_index] = copy_price_s2
    #     chro_sales[max_index] = copy_sales_s2
    #     chro_profit[max_index] = copy_profit_s2
    #     chro_new[max_index] = copy_new_s2
    #     chro_cargolane_occupied[max_index] = copy_occupied_s2
    #     chro_recommend_prod[max_index] = copy_recommend_s2

    #     chro[sec_index] = copy_s1
    #     chro_price[sec_index] = copy_price_s1
    #     chro_sales[sec_index] = copy_sales_s1
    #     chro_profit[sec_index] = copy_profit_s1
    #     chro_new[sec_index] = copy_new_s1
    #     chro_cargolane_occupied[sec_index] = copy_occupied_s1
    #     chro_recommend_prod[sec_index] = copy_recommend_s1
    
    cross_points = [np.random.randint(0, len(chro[0])-1)]
    crossover_rate = 0.84 #!!!!!
    
    list_random=[]
    list_random.clear()
    for i in range(len(chro[0])):
        cross_rd = random.random()
        list_random.append(cross_rd)

    copy_s1 = selection1.copy()
    copy_profit_s1 = selection1_profit.copy()
    copy_price_s1 = selection1_price.copy()
    copy_sales_s1 = selection1_sales.copy()
    copy_new_s1 = selection1_new.copy()
    copy_occupied_s1 = selection1_occupied.copy()
    copy_recommend_s1 = selection1_recommend.copy()
    copy_inventory_cost_s1= selection1_inventory_cost.copy()
    copy_backroom_cost_s1= selection1_backroom_cost.copy()
    copy_display_cost_s1= selection1_display_cost.copy()
    copy_ordering_cost_s1= selection1_ordering_cost.copy()
    copy_purchasing_cost_s1= selection1_purchasing_cost.copy()
    copy_replenishment_s1= selection1_replenishment.copy()
    copy_stockout_s1= selection1_stockout.copy()
    copy_lostsales_s1= selection1_lostsales.copy()
    copy_quantity_display_s1 = selection1_qty_displayed.copy()
    
    copy_s2 = selection2.copy()
    copy_profit_s2 = selection2_profit.copy()
    copy_price_s2 = selection2_price.copy()
    copy_sales_s2 = selection2_sales.copy()
    copy_new_s2 = selection2_new.copy()
    copy_occupied_s2 = selection2_occupied.copy()
    copy_recommend_s2 = selection2_recommend.copy()
    copy_inventory_cost_s2= selection2_inventory_cost.copy()
    copy_backroom_cost_s2= selection2_backroom_cost.copy()
    copy_display_cost_s2= selection2_display_cost.copy()
    copy_ordering_cost_s2= selection2_ordering_cost.copy()
    copy_purchasing_cost_s2= selection2_purchasing_cost.copy()
    copy_replenishment_s2= selection2_replenishment.copy()
    copy_stockout_s2= selection2_stockout.copy()
    copy_lostsales_s2= selection2_lostsales.copy()
    copy_quantity_display_s2 = selection2_qty_displayed.copy()

    
    temp_s1 = selection1.copy()
    temp_profit_s1 = selection1_profit.copy()
    temp_price_s1 = selection1_price.copy()
    temp_sales_s1 = selection1_sales.copy()
    temp_new_s1 = selection1_new.copy()
    temp_occupied_s1 = selection1_occupied.copy()
    temp_recommend_s1 = selection1_recommend.copy()
    temp_inventory_cost_s1= selection1_inventory_cost.copy()
    temp_backroom_cost_s1= selection1_backroom_cost.copy()
    temp_display_cost_s1= selection1_display_cost.copy()
    temp_ordering_cost_s1= selection1_ordering_cost.copy()
    temp_purchasing_cost_s1= selection1_purchasing_cost.copy()
    temp_replenishment_s1= selection1_replenishment.copy()
    temp_stockout_s1= selection1_stockout.copy()
    temp_lostsales_s1= selection1_lostsales.copy()
    temp_quantity_display_s1 = selection1_qty_displayed.copy()

    
    
    for i in range(len(chro[0])):
       
        s1isoccu = CargoLane_ID[i] in copy_occupied_s1 # True = 該貨道是推薦品項 & cross為index, 所以要+1
        s2isoccu = CargoLane_ID[i] in copy_occupied_s2
        
        if s1isoccu == True and s2isoccu == True: # 兩個都是推薦品項, 才換
            if list_random[i]< crossover_rate:
               
                copy_s1[i] = copy_s2[i]
                copy_s2[i] = temp_s1[i]
                
                copy_profit_s1[i] = copy_profit_s2[i]
                copy_profit_s2[i] = temp_profit_s1[i]
                
                copy_price_s1[i] = copy_price_s2[i]
                copy_price_s2[i] = temp_price_s1[i]
                
                copy_sales_s1[i] = copy_sales_s2[i]
                copy_sales_s2[i] = temp_sales_s1[i]
                
                copy_new_s1[i] = copy_new_s2[i]
                copy_new_s2[i] = temp_new_s1[i]
               
                copy_recommend_s1[copy_occupied_s1.index(CargoLane_ID[i])] = copy_recommend_s2[copy_occupied_s2.index(CargoLane_ID[i])]
                copy_recommend_s2[copy_occupied_s2.index(CargoLane_ID[i])] = temp_recommend_s1[temp_occupied_s1.index(CargoLane_ID[i])]
              
                copy_inventory_cost_s1[i]= copy_inventory_cost_s2[i]
                copy_inventory_cost_s2[i]= temp_inventory_cost_s1[i]
                
                copy_backroom_cost_s1[i]= copy_backroom_cost_s2[i]
                copy_backroom_cost_s2[i]= temp_backroom_cost_s1[i]
                
                copy_display_cost_s1[i]= copy_display_cost_s2[i]
                copy_display_cost_s2[i]= temp_display_cost_s1[i]
                
                copy_ordering_cost_s1[i]= copy_ordering_cost_s2[i]
                copy_ordering_cost_s2[i]= temp_ordering_cost_s1[i]
                
                copy_purchasing_cost_s1[i]= copy_purchasing_cost_s2[i]
                copy_purchasing_cost_s2[i]= temp_purchasing_cost_s1[i]
                
                copy_replenishment_s1[i]= copy_replenishment_s2[i]
                copy_replenishment_s2[i]= temp_replenishment_s1[i]
                
                copy_stockout_s1[i]= copy_stockout_s2[i]
                copy_stockout_s2[i]= temp_stockout_s1[i]
                
                copy_lostsales_s1[i]= copy_lostsales_s2[i]
                copy_lostsales_s2[i]= temp_lostsales_s1[i]
                
                copy_quantity_display_s1[i] = copy_quantity_display_s2[i]
                copy_quantity_display_s2[i] = temp_quantity_display_s1[i]
                
                
            elif list_random[i] >= crossover_rate:
                pass
            
        elif s1isoccu == False and s2isoccu == False: # 兩個都不是推薦品項, 才換
            if list_random[i]< crossover_rate:
               
                copy_s1[i] = copy_s2[i]
                copy_s2[i] = temp_s1[i]

                copy_profit_s1[i] = copy_profit_s2[i]
                copy_profit_s2[i] = temp_profit_s1[i]
                
                copy_price_s1[i] = copy_price_s2[i]
                copy_price_s2[i] = temp_price_s1[i]
                
                copy_sales_s1[i] = copy_sales_s2[i]
                copy_sales_s2[i] = temp_sales_s1[i]
                
                copy_new_s1[i] = copy_new_s2[i]
                copy_new_s2[i] = temp_new_s1[i]
                
                copy_inventory_cost_s1[i]= copy_inventory_cost_s2[i]
                copy_inventory_cost_s2[i]= temp_inventory_cost_s1[i]
                
                copy_backroom_cost_s1[i]= copy_backroom_cost_s2[i]
                copy_backroom_cost_s2[i]= temp_backroom_cost_s1[i]
                
                copy_display_cost_s1[i]= copy_display_cost_s2[i]
                copy_display_cost_s2[i]= temp_display_cost_s1[i]
                
                copy_ordering_cost_s1[i]= copy_ordering_cost_s2[i]
                copy_ordering_cost_s2[i]= temp_ordering_cost_s1[i]
                
                copy_purchasing_cost_s1[i]= copy_purchasing_cost_s2[i]
                copy_purchasing_cost_s2[i]= temp_purchasing_cost_s1[i]
                
                copy_replenishment_s1[i]= copy_replenishment_s2[i]
                copy_replenishment_s2[i]= temp_replenishment_s1[i]
                
                copy_stockout_s1[i]= copy_stockout_s2[i]
                copy_stockout_s2[i]= temp_stockout_s1[i]
                
                copy_lostsales_s1[i]= copy_lostsales_s2[i]
                copy_lostsales_s2[i]= temp_lostsales_s1[i]
                
                copy_quantity_display_s1[i] = copy_quantity_display_s2[i]
                copy_quantity_display_s2[i] = temp_quantity_display_s1[i]
                
            elif list_random[i] >= crossover_rate:
                  pass
    # 如果只要相符就直接替換, 不管結果是否比較好
 
        
    profit1_matrix = pd.DataFrame({"ID": copy_s1, "Profit": copy_profit_s1})
    profit1_matrix_without_duplicates = profit1_matrix.drop_duplicates(subset = ["ID", "Profit"])
    #profit1 = (sum(profit1_matrix_without_duplicates["Profit"]))
    profit1 = (sum(profit1_matrix["Profit"]))
    
    profit2_matrix = pd.DataFrame({"ID": copy_s2, "Profit": copy_profit_s2})
    profit2_matrix_without_duplicates = profit2_matrix.drop_duplicates(subset = ["ID", "Profit"])
    #profit2 = (sum(profit2_matrix_without_duplicates["Profit"]))
    profit2 = (sum(profit2_matrix["Profit"]))
    
    whichbigger = profit1 > profit2
    if whichbigger == True: #profit1 bigger
        chro[max_index] = copy_s1
        chro_price[max_index] = copy_price_s1
        chro_sales[max_index] = copy_sales_s1
        chro_profit[max_index] = copy_profit_s1
        chro_new[max_index] = copy_new_s1
        chro_cargolane_occupied[max_index] = copy_occupied_s1
        chro_recommend_prod[max_index] = copy_recommend_s1
        chro_inventory_cost[max_index]= copy_inventory_cost_s1
        chro_backroom_cost[max_index]= copy_backroom_cost_s1
        chro_display_cost[max_index]= copy_display_cost_s1
        chro_ordering_cost[max_index]= copy_ordering_cost_s1
        chro_purchasing_cost[max_index]= copy_purchasing_cost_s1
        chro_replenishment[max_index]= copy_replenishment_s1
        chro_stockout[max_index]= copy_stockout_s1
        chro_lostsales[max_index]= copy_lostsales_s1
        chro_quantity_display[max_index]= copy_quantity_display_s1
        
        chro[sec_index] = copy_s2
        chro_price[sec_index] = copy_price_s2
        chro_sales[sec_index] = copy_sales_s2
        chro_profit[sec_index] = copy_profit_s2
        chro_new[sec_index] = copy_new_s2
        chro_cargolane_occupied[sec_index] = copy_occupied_s2
        chro_recommend_prod[sec_index] = copy_recommend_s2
        chro_inventory_cost[sec_index]= copy_inventory_cost_s2
        chro_backroom_cost[sec_index]= copy_backroom_cost_s2
        chro_display_cost[sec_index]= copy_display_cost_s2
        chro_ordering_cost[sec_index]= copy_ordering_cost_s2
        chro_purchasing_cost[sec_index]= copy_purchasing_cost_s2
        chro_replenishment[sec_index]= copy_replenishment_s2
        chro_stockout[sec_index]= copy_stockout_s2
        chro_lostsales[sec_index]= copy_lostsales_s2
        chro_quantity_display[sec_index] = copy_quantity_display_s2
        
    else: #profit2 bigger
        chro[max_index] = copy_s2
        chro_price[max_index] = copy_price_s2
        chro_sales[max_index] = copy_sales_s2
        chro_profit[max_index] = copy_profit_s2
        chro_new[max_index] = copy_new_s2
        chro_cargolane_occupied[max_index] = copy_occupied_s2
        chro_recommend_prod[max_index] = copy_recommend_s2
        chro_inventory_cost[max_index]= copy_inventory_cost_s2
        chro_backroom_cost[max_index]= copy_backroom_cost_s2
        chro_display_cost[max_index]= copy_display_cost_s2
        chro_ordering_cost[max_index]= copy_ordering_cost_s2
        chro_purchasing_cost[max_index]= copy_purchasing_cost_s2
        chro_replenishment[max_index]= copy_replenishment_s2
        chro_stockout[max_index]= copy_stockout_s2
        chro_lostsales[max_index]= copy_lostsales_s2
        chro_quantity_display[max_index]= copy_quantity_display_s2
        
        chro[sec_index] = copy_s1
        chro_price[sec_index] = copy_price_s1
        chro_sales[sec_index] = copy_sales_s1
        chro_profit[sec_index] = copy_profit_s1
        chro_new[sec_index] = copy_new_s1
        chro_cargolane_occupied[sec_index] = copy_occupied_s1
        chro_recommend_prod[sec_index] = copy_recommend_s1
        chro_inventory_cost[sec_index]= copy_inventory_cost_s1
        chro_backroom_cost[sec_index]= copy_backroom_cost_s1
        chro_display_cost[sec_index]= copy_display_cost_s1
        chro_ordering_cost[sec_index]= copy_ordering_cost_s1
        chro_purchasing_cost[sec_index]= copy_purchasing_cost_s1
        chro_replenishment[sec_index]= copy_replenishment_s1
        chro_stockout[sec_index]= copy_stockout_s1
        chro_lostsales[sec_index]= copy_lostsales_s1
        chro_quantity_display[sec_index]= copy_quantity_display_s1
       
     ################################################################################################################################################
    # if whichbigger == True: #profit1 bigger
    #     if profit1 - oppoloss(Demand_Product_ID, copy_s1, copy_occupied_s1) > each_chro_profit_withloss[max_index]:
    #         chro[max_index] = copy_s1
    #         chro_price[max_index] = copy_price_s1
    #         chro_sales[max_index] = copy_sales_s1
    #         chro_profit[max_index] = copy_profit_s1
    #         chro_new[max_index] = copy_new_s1
    #         chro_cargolane_occupied[max_index] = copy_occupied_s1
    #         chro_recommend_prod[max_index] = copy_recommend_s1
    #     elif profit2 - oppoloss(Demand_Product_ID, copy_s2, copy_occupied_s2) > each_chro_profit_withloss[sec_index]:
    #         chro[sec_index] = copy_s2
    #         chro_price[sec_index] = copy_price_s2
    #         chro_sales[sec_index] = copy_sales_s2
    #         chro_profit[sec_index] = copy_profit_s2
    #         chro_new[sec_index] = copy_new_s2
    #         chro_cargolane_occupied[sec_index] = copy_occupied_s2
    #         chro_recommend_prod[sec_index] = copy_recommend_s2
    # else: #profit2 bigger
    #     if profit2 - oppoloss(Demand_Product_ID, copy_s2, copy_occupied_s2) > each_chro_profit_withloss[max_index]:
    #         chro[max_index] = copy_s2
    #         chro_price[max_index] = copy_price_s2
    #         chro_sales[max_index] = copy_sales_s2
    #         chro_profit[max_index] = copy_profit_s2
    #         chro_new[max_index] = copy_new_s2
    #         chro_cargolane_occupied[max_index] = copy_occupied_s2
    #         chro_recommend_prod[max_index] = copy_recommend_s2
    #     elif profit1 - oppoloss(Demand_Product_ID, copy_s1, copy_occupied_s1) > each_chro_profit_withloss[sec_index]:
    #         chro[sec_index] = copy_s1
    #         chro_price[sec_index] = copy_price_s1
    #         chro_sales[sec_index] = copy_sales_s1
    #         chro_profit[sec_index] = copy_profit_s1
    #         chro_new[sec_index] = copy_new_s1
    #         chro_cargolane_occupied[sec_index] = copy_occupied_s1
    #         chro_recommend_prod[sec_index] = copy_recommend_s1
        
    # return chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod
    return copy_s1, copy_price_s1, copy_sales_s1, copy_profit_s1, copy_new_s1, copy_occupied_s1, copy_recommend_s1, copy_inventory_cost_s1, copy_backroom_cost_s1, copy_display_cost_s1, copy_ordering_cost_s1, copy_purchasing_cost_s1, copy_replenishment_s1, copy_stockout_s1, copy_lostsales_s1, copy_quantity_display_s1,\
        copy_s2, copy_price_s2, copy_sales_s2, copy_profit_s2, copy_new_s2, copy_occupied_s2, copy_recommend_s2, copy_inventory_cost_s2, copy_backroom_cost_s2, copy_display_cost_s2, copy_ordering_cost_s2, copy_purchasing_cost_s2, copy_replenishment_s2, copy_stockout_s2, copy_lostsales_s2, copy_quantity_display_s2

#%%
# GA mutation
#def mutation(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, each_chro_profit_withloss, ID1, ID2, ID3, ID4, ID5, price1, price2, price3, price4, price5, IDs1, IDs2, IDs3, IDs4, prices1, prices2, prices3, prices4, Cargolane_ID,Product_Cost, setup_cost, replenishment_cost, total_cost):
def mutation(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_inventory_cost,selection1_backroom_cost,selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, ID1, ID2, ID3, ID4, ID5, price1, price2, price3, price4, price5, IDs1, IDs2, IDs3, IDs4, prices1, prices2, prices3, prices4,Cargolane_ID):
   
    mutation_rate = 0.0579 #!!!!!
    mutationran = [random.random(), random.random()]
    

    # print("chro", chro_cargolane_occupied)
    # cross_matrix=[]
    # sjmn=[]
    # for i in range(len(chro)):
    #     cross_elasticity=[]
    #     random.seed()
    #     selectionID = chro[i]
    #     for i in range(len(selectionID)):
    #         rando = random.uniform(-0.05, 0.05)
    #         rando=round(rando,3)
    #         cross_elasticity.append(rando)
    #     cross_matrix.append(cross_elasticity)
        
    # for i in range(len(selectionID)):
    #     cross_matrix[i][i]=0.0
    # # print("crossmatrix", cross_matrix)
    
    # capacity_arr=[]
    # for i in range(len(selectionID)):
    #     capacity_arr.append(selection1_qty_displayed)
    # sjm_matrix= np.power(capacity_arr,cross_matrix)
    # # print("sjm_matrix", sjm_matrix)
    
    # for i in range(len(sjm_matrix)):
    #     f=np.prod(sjm_matrix[i])
    #     sjmn.append(f)
    
    mean = 0  # Mean of the normal distribution
    std = 1  # Standard deviation of the normal distribution
    # Generate stochastic demand values
    # experror = []
    error = random.normalvariate(mean, std)  # Generate random error term
    experror = math.exp(error)
    # experror.append(error1)
    
        
    #recommended_profit_ratio = 1/5
    recommended_profit_ratio = 1
    alpha= random.uniform(5, 10)
    space_elas= random.uniform(0.2,0.4)
    cross_elas= random.uniform(-0.05,0.05)
    problostsales=0.1
    
    def cm(replacement_matrix, ranID):  #constraints matrix
        if ranID in replacement_matrix.keys():
            replaceID = replacement_matrix[ranID]
          
            
            if replaceID in ID1:
                del price1[ID1.index(replaceID)]
                del ID1[ID1.index(replaceID)]
            if replaceID in ID2:
                del price2[ID2.index(replaceID)]
                del ID2[ID2.index(replaceID)]
            if replaceID in ID3:
                del price3[ID3.index(replaceID)]
                del ID3[ID3.index(replaceID)]
            if replaceID in ID4:
                del price4[ID4.index(replaceID)]
                del ID4[ID4.index(replaceID)]
            if replaceID in ID5:
                del price5[ID5.index(replaceID)]
                del ID5[ID5.index(replaceID)]
            # s
            if replaceID in IDs1:
                del prices1[IDs1.index(replaceID)]
                del IDs1[IDs1.index(replaceID)]
            if replaceID in IDs2:
                del prices2[IDs2.index(replaceID)]
                del IDs2[IDs2.index(replaceID)]
            if replaceID in IDs3:
                del prices3[IDs3.index(replaceID)]
                del IDs3[IDs3.index(replaceID)]
            if replaceID in IDs4:
                del prices4[IDs4.index(replaceID)]
                del IDs4[IDs4.index(replaceID)]
                
    for i in selection1:
        cm(replacement_matrix, i)
        #print(cm)
        
    for i in selection2:
        cm(replacement_matrix, i)
        
    
        
    #************************************ Cargolane Occupied only ******************************************************************

    # if mutationran[0] < mutation_rate and selection1_occupied != []:
    #     candidate_index = CargoLane_ID.index(choice(selection1_occupied)) # index of chro list
    #     # candidate_index = choice(selection1_occupied) - 1 # index of chro list
    #     if CargoLane_Type[candidate_index] == 0:
    #         pass
    #     elif CargoLane_Type[candidate_index] == 1:
    #         re_ID = choice(ID1)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == 2:
    #         re_ID = choice(ID2)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == 3:
    #         re_ID = choice(ID3)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == 4:
    #         re_ID = choice(ID4)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == 5:
    #         re_ID = choice(ID5)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == "s1.0" or CargoLane_Type[candidate_index] == "s1":
    #         re_ID = choice(IDs1)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == "s2.0" or CargoLane_Type[candidate_index] == "s2":
    #         re_ID = choice(IDs2)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == "s3.0" or CargoLane_Type[candidate_index] == "s3":
    #         re_ID = choice(IDs3)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
    #     elif CargoLane_Type[candidate_index] == "s4.0" or CargoLane_Type[candidate_index] == "s4":
    #         re_ID = choice(IDs4)
    #         selection1[candidate_index] = re_ID
    #         selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
    #         selection1_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection1_sales[candidate_index]= alpha* (selection1_qty_displayed**space_elas) * (selection1_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed+sqrt(selection1_sales[candidate_index]))
    #         selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]
    #         selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed
    #         selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index]) * recommended_profit_ratio
            
    #         selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
    #         selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index])] = re_ID
            
            
    # elif mutationran[1] < mutation_rate and selection2_occupied != []:
    #     candidate_index2 = CargoLane_ID.index(choice(selection2_occupied)) # index of chro list
    #     if CargoLane_Type[candidate_index2] == 0:
    #         pass
    #     elif CargoLane_Type[candidate_index2] == 1:
    #         re_ID = choice(ID1)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         # selection2_recommend[selection2_occupied.index(candidate_index2 + 1)] = re_ID
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == 2:
    #         re_ID = choice(ID2)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == 3:
    #         re_ID = choice(ID3)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
    #         if mode == str(2):
    #             selection2_sales[candidate_index2] = Demand_Product_Sales[Demand_Product_ID.index(re_ID)] * recommended_profit_ratio
    #             selection2_profit[candidate_index2] = ((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * Product_Product_sales[Product_ID.index(re_ID)])* recommended_profit_ratio
    #         elif mode == str(3):
    #             selection2_sales[candidate_index2] = Product_Product_sales[Product_ID.index(re_ID)] * recommended_profit_ratio
    #             selection2_profit[candidate_index2] = ((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * Product_Product_sales[Product_ID.index(re_ID)]) * recommended_profit_ratio
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == 4:
    #         re_ID = choice(ID4)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == 5:
    #         re_ID = choice(ID5)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == "s1.0" or CargoLane_Type[candidate_index2] == "s1":
    #         re_ID = choice(IDs1)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == "s2.0" or CargoLane_Type[candidate_index2] == "s2":
    #         re_ID = choice(IDs2)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == "s3.0" or CargoLane_Type[candidate_index2] == "s3":
    #         re_ID = choice(IDs3)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    #     elif CargoLane_Type[candidate_index2] == "s4.0" or CargoLane_Type[candidate_index2] == "s4":
    #         re_ID = choice(IDs4)
    #         selection2[candidate_index2] = re_ID
    #         selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            
    #         selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
    #         selection2_qty_displayed= CargoLane_Diameter_Max_1[Product_ID.index(re_ID)]/Product_Length[Product_ID.index(re_ID)]
    #         selection2_sales[candidate_index2]= alpha* (selection2_qty_displayed**space_elas) * (selection2_qty_displayed**cross_elas) * recommended_profit_ratio
    #         selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed+sqrt(selection2_sales[candidate_index2]))
    #         selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]
    #         selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed
    #         selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]
    #         selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2]) * recommended_profit_ratio
            
    #         selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
    #         selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2])] = re_ID
    
    
    # chro[max_index] = selection1
    # chro_price[max_index] = selection1_price
    # chro_sales[max_index] = selection1_sales
    # chro_profit[max_index] = selection1_profit
    # chro_new[max_index] = selection1_new
    # chro_cargolane_occupied[max_index] = selection1_occupied
    # chro_recommend_prod[max_index] = selection1_recommend
    # chro_inventory_cost[max_index] =selection1_inventory_cost
    # chro_backroom_cost[max_index] = selection1_backroom_cost
    # chro_display_cost[max_index] = selection1_display_cost
    # chro_ordering_cost[max_index] = selection1_ordering_cost
    # chro_purchasing_cost[max_index] = selection1_purchasing_cost
    
    # chro[sec_index] = selection2
    # chro_price[sec_index] = selection2_price
    # chro_sales[sec_index] = selection2_sales
    # chro_profit[sec_index] = selection2_profit
    # chro_new[sec_index] = selection2_new
    # chro_cargolane_occupied[sec_index] = selection2_occupied
    # chro_recommend_prod[sec_index] = selection2_recommend
    # chro_inventory_cost[sec_index] = selection2_inventory_cost
    # chro_backroom_cost[sec_index] = selection2_backroom_cost
    # chro_display_cost[sec_index] = selection2_display_cost
    # chro_ordering_cost[sec_index] = selection2_ordering_cost
    # chro_purchasing_cost[sec_index] = selection2_purchasing_cost
    
    #************************************ All Cargolane ******************************************************************
    if mutationran[0] < mutation_rate and Cargolane_ID != []:
        candidate_index = CargoLane_ID.index(choice(Cargolane_ID)) # index of chro list
        # candidate_index = choice(selection1_occupied) - 1 # index of chro list
        if CargoLane_Type[candidate_index] == 0:
            pass
        elif CargoLane_Type[candidate_index] == 1:
            re_ID = choice(ID1)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
    
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index] * selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
                
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror * recommended_profit_ratio,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == 2:
            re_ID = choice(ID2)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
    
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
                
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror * recommended_profit_ratio,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == 3:
            re_ID = choice(ID3)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
           
   
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
               
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas)* experror * recommended_profit_ratio,10))
                selection1_replenishment[candidate_index]= (round(sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / ((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= ((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*selection1_stockout[candidate_index]*selection1_replenishment[candidate_index])
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == 4:
            re_ID = choice(ID4)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
           
   
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
               
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror* recommended_profit_ratio,10))
                selection1_replenishment[candidate_index]= (round(sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / ((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= ((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*selection1_stockout[candidate_index]*selection1_replenishment[candidate_index])
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == 5:
            re_ID = choice(ID5)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
   
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
               
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror* recommended_profit_ratio,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == "s1.0" or CargoLane_Type[candidate_index] == "s1":
            re_ID = choice(IDs1)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
           
   
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
               
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror* recommended_profit_ratio,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == "s2.0" or CargoLane_Type[candidate_index] == "s2":
            re_ID = choice(IDs2)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
           
   
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
               
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror* recommended_profit_ratio,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == "s3.0" or CargoLane_Type[candidate_index] == "s3":
            re_ID = choice(IDs3)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)]
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
   
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
               
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror * recommended_profit_ratio,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index] == "s4.0" or CargoLane_Type[candidate_index] == "s4":
            re_ID = choice(IDs4)
            selection1[candidate_index] = re_ID
            selection1_price[candidate_index] = Product_Price[Product_ID.index(re_ID)] 
            selection1_new[candidate_index] = Product_New[Product_ID.index(re_ID)]
            selection1_purchasing_cost[candidate_index]= Product_Cost[Product_ID.index(re_ID)]
            selection1_qty_displayed[candidate_index]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
   
            if candidate_index not in selection1_occupied:
                selection1_recommend=selection1_recommend
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio
               
            elif candidate_index in selection1_occupied:
                selection1_recommend[selection1_occupied.index(CargoLane_ID[candidate_index]-1)] = re_ID
                selection1_sales[candidate_index]= round(max(alpha* (selection1_qty_displayed[candidate_index]**space_elas) * (selection1_qty_displayed[candidate_index]**cross_elas) * experror * recommended_profit_ratio,1))
                selection1_replenishment[candidate_index]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index])),1)))
                selection1_stockout[candidate_index]= (round(max(selection1_sales[candidate_index]-selection1_qty_displayed[candidate_index],0)))
                selection1_lostsales[candidate_index]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection1_sales[candidate_index]*selection1_replenishment[candidate_index]-selection1_qty_displayed[candidate_index]),0)
                selection1_inventory_cost[candidate_index]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection1_qty_displayed[candidate_index]+(selection1_sales[candidate_index]* selection1_replenishment[candidate_index]/2))
                selection1_backroom_cost[candidate_index]= unit_backroom_cost[Product_ID.index(re_ID)]* selection1_sales[candidate_index]* selection1_replenishment[candidate_index]
                selection1_display_cost[candidate_index]= unit_display_cost[Product_ID.index(re_ID)] * selection1_qty_displayed[candidate_index]* selection1_replenishment[candidate_index]
                selection1_ordering_cost[candidate_index]= unit_ordering_cost[Product_ID.index(re_ID)] / selection1_replenishment[candidate_index]
                selection1_profit[candidate_index] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection1_sales[candidate_index]* selection1_replenishment[candidate_index]) - selection1_inventory_cost[candidate_index]- selection1_backroom_cost[candidate_index] - selection1_display_cost[candidate_index]- selection1_ordering_cost[candidate_index] - selection1_lostsales[candidate_index]) * recommended_profit_ratio

    elif mutationran[1] < mutation_rate and Cargolane_ID != []:
        candidate_index2 = CargoLane_ID.index(choice(Cargolane_ID)) # index of chro list
        if CargoLane_Type[candidate_index2] == 0:
            pass
        elif CargoLane_Type[candidate_index2] == 1:
            re_ID = choice(ID1)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2] *selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == 2:
            re_ID = choice(ID2)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == 3:
            re_ID = choice(ID3)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == 4:
            re_ID = choice(ID4)
            selection2[candidate_index2] = re_ID  
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == 5:
            re_ID = choice(ID5)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == "s1.0" or CargoLane_Type[candidate_index2] == "s1":
            re_ID = choice(IDs1)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]  
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == "s2.0" or CargoLane_Type[candidate_index2] == "s2":
            re_ID = choice(IDs2)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
            
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == "s3.0" or CargoLane_Type[candidate_index2] == "s3":
            re_ID = choice(IDs3)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror*recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio

        elif CargoLane_Type[candidate_index2] == "s4.0" or CargoLane_Type[candidate_index2] == "s4":
            re_ID = choice(IDs4)
            selection2[candidate_index2] = re_ID
            selection2_price[candidate_index2] = Product_Price[Product_ID.index(re_ID)]
            selection2_new[candidate_index2] = Product_New[Product_ID.index(re_ID)]
            selection2_purchasing_cost[candidate_index2]= Product_Cost[Product_ID.index(re_ID)]
            selection2_qty_displayed[candidate_index2]= round(CargoLane_Diameter_Max_1[0]/Product_Length[Product_ID.index(re_ID)])
             
            if candidate_index2 not in selection2_occupied:
                selection2_recommend=selection2_recommend
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
                
                
            elif candidate_index2 in selection2_occupied:
                selection2_recommend[selection2_occupied.index(CargoLane_ID[candidate_index2]-1)] = re_ID
                selection2_sales[candidate_index2]= round(max(alpha* (selection2_qty_displayed[candidate_index2]**space_elas) * (selection2_qty_displayed[candidate_index2]**cross_elas) * experror *recommended_profit_ratio,1))
                selection2_replenishment[candidate_index2]= (round(max(math.sqrt(unit_ordering_cost[Product_ID.index(re_ID)] / (((unit_inventory_cost[Product_ID.index(re_ID)]/2) + unit_backroom_cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2])),1)))
                selection2_stockout[candidate_index2]= (round(max(selection2_sales[candidate_index2]-selection2_qty_displayed[candidate_index2],0)))
                selection2_lostsales[candidate_index2]= max((Product_Price[Product_ID.index(re_ID)]- Product_Cost[Product_ID.index(re_ID)])*(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]-selection2_qty_displayed[candidate_index2]),0)
                selection2_inventory_cost[candidate_index2]= unit_inventory_cost[Product_ID.index(re_ID)]* (selection2_qty_displayed[candidate_index2]+(selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]/2))
                selection2_backroom_cost[candidate_index2]= unit_backroom_cost[Product_ID.index(re_ID)]* selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_display_cost[candidate_index2]= unit_display_cost[Product_ID.index(re_ID)] * selection2_qty_displayed[candidate_index2]*selection2_replenishment[candidate_index2]
                selection2_ordering_cost[candidate_index2]= unit_ordering_cost[Product_ID.index(re_ID)]/selection2_replenishment[candidate_index2]
                selection2_profit[candidate_index2] = (((Product_Price[Product_ID.index(re_ID)] - Product_Cost[Product_ID.index(re_ID)]) * selection2_sales[candidate_index2]*selection2_replenishment[candidate_index2]) - selection2_inventory_cost[candidate_index2]- selection2_backroom_cost[candidate_index2] - selection2_display_cost[candidate_index2]- selection2_ordering_cost[candidate_index2] - selection2_lostsales[candidate_index2]) * recommended_profit_ratio
    
    chro[max_index] = selection1
    chro_price[max_index] = selection1_price
    chro_sales[max_index] = selection1_sales
    chro_profit[max_index] = selection1_profit
    chro_new[max_index] = selection1_new
    chro_cargolane_occupied[max_index] = selection1_occupied
    chro_recommend_prod[max_index] = selection1_recommend
    chro_inventory_cost[max_index] =selection1_inventory_cost
    chro_backroom_cost[max_index] = selection1_backroom_cost
    chro_display_cost[max_index] = selection1_display_cost
    chro_ordering_cost[max_index] = selection1_ordering_cost
    chro_purchasing_cost[max_index] = selection1_purchasing_cost
    chro_replenishment[max_index]= selection1_replenishment
    chro_stockout[max_index]= selection1_stockout
    chro_lostsales[max_index]= selection1_lostsales
    chro_quantity_display[max_index]= selection1_qty_displayed
    
    chro[sec_index] = selection2
    chro_price[sec_index] = selection2_price
    chro_sales[sec_index] = selection2_sales
    chro_profit[sec_index] = selection2_profit
    chro_new[sec_index] = selection2_new
    chro_cargolane_occupied[sec_index] = selection2_occupied
    chro_recommend_prod[sec_index] = selection2_recommend
    chro_inventory_cost[sec_index] = selection2_inventory_cost
    chro_backroom_cost[sec_index] = selection2_backroom_cost
    chro_display_cost[sec_index] = selection2_display_cost
    chro_ordering_cost[sec_index] = selection2_ordering_cost
    chro_purchasing_cost[sec_index] = selection2_purchasing_cost
    chro_replenishment[sec_index]= selection2_replenishment
    chro_stockout[sec_index]= selection2_stockout
    chro_lostsales[sec_index]= selection2_lostsales
    chro_quantity_display[sec_index]= selection2_qty_displayed

    # return chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod
    return selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend,selection1_purchasing_cost,selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_sales,selection1_inventory_cost,selection1_backroom_cost,selection1_display_cost, selection1_ordering_cost, \
        selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_purchasing_cost,selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_sales,selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost
#%%

#def GA(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, each_chro_profit, oppo_loss_list, each_chro_profit_withloss): # , ID1, ID2, ID3, ID4, ID5, price1, price2, price3, price4, price5, IDs1, IDs2, IDs3, IDs4, prices1, prices2, prices3, prices4
def GA(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit): # , ID1, ID2, ID3, ID4, ID5, price1, price2, price3, price4, price5, IDs1, IDs2, IDs3, IDs4, prices1, prices2, prices3, prices4
    
    new_chro = []
    new_chro_price = []
    new_chro_sales = []
    new_chro_profit = []
    new_chro_new = []
    new_chro_cargolane_occupied = []
    new_chro_recommend_prod = []
    new_chro_inventory_cost=[]
    new_chro_backroom_cost=[]
    new_chro_display_cost=[]
    new_chro_ordering_cost=[]
    new_chro_purchasing_cost=[]
    new_chro_replenishment=[]
    new_chro_stockout=[]
    new_chro_lostsales=[]
    new_chro_quantity_display=[]
    
    #fitness = copy.deepcopy(each_chro_profit_withloss)
    fitness = copy.deepcopy(each_chro_profit)
    # print("atas",fitness)
    
    index11 = fitness.index(max(fitness))
    fitness[index11] = 0
    index22 = fitness.index(max(fitness))
    # print(index11)
    # print(index22)
    
    for i in [index11, index22]:
        new_chro.append(chro[i])
        new_chro_price.append(chro_price[i])
        new_chro_sales.append(chro_sales[i])
        new_chro_profit.append(chro_profit[i])
        new_chro_new.append(chro_new[i])
        new_chro_cargolane_occupied.append(chro_cargolane_occupied[i])
        new_chro_recommend_prod.append(chro_recommend_prod[i])
        new_chro_inventory_cost.append(chro_inventory_cost[i])
        new_chro_backroom_cost.append(chro_backroom_cost[i])
        new_chro_display_cost.append(chro_display_cost[i])
        new_chro_ordering_cost.append(chro_ordering_cost[i])
        new_chro_purchasing_cost.append(chro_purchasing_cost[i])
        new_chro_replenishment.append(chro_replenishment[i])
        new_chro_stockout.append(chro_stockout[i])
        new_chro_lostsales.append(chro_lostsales[i])
        new_chro_quantity_display.append(chro_quantity_display[i])
    # print(new_chro)
    
    onemax_onerou = int(round((len(chro)-2)/2/2,0))
    tworou = int((len(chro)-2)/2 - int(round((len(chro)-2)/2/2,0)))
    # print(len(chro))
    # print(chro)
    # print(range(onemax_onerou))
    # print(tworou)
    
    
    # for j in range(len(chro)-2):
    for j in range(onemax_onerou):
        selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost,selection1_ordering_cost, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_inventory_cost, selection2_backroom_cost, selection2_display_cost,selection2_ordering_cost, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, max_index, sec_index = selection(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit)
        selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost,selection1_ordering_cost, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_inventory_cost, selection2_backroom_cost, selection2_display_cost,selection2_ordering_cost, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed = crossover(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod,chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost,selection1_ordering_cost, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new,selection2_inventory_cost, selection2_backroom_cost, selection2_display_cost,selection2_ordering_cost, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend)
        if mode == str(2):
            selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend,selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_sales,selection1_inventory_cost,selection1_backroom_cost,selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_sales,selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost = mutation(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, CargoLane_ID)
        if mode == str(3):
            selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend,selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_sales,selection1_inventory_cost,selection1_backroom_cost,selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_sales,selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost = mutation(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, CargoLane_ID)
        for i in [1, 2]:
            new_chro.append(locals() ["selection" + str(i)])
            new_chro_price.append(locals() ["selection" + str(i) + "_price"])
            new_chro_sales.append(locals() ["selection" + str(i) + "_sales"])
            new_chro_profit.append(locals() ["selection" + str(i) + "_profit"])
            new_chro_new.append(locals() ["selection" + str(i) + "_new"])
            new_chro_cargolane_occupied.append(locals() ["selection" + str(i) + "_occupied"])
            new_chro_recommend_prod.append(locals() ["selection" + str(i) + "_recommend"])
            new_chro_inventory_cost.append(locals() ["selection" + str(i) + "_inventory_cost"])
            new_chro_backroom_cost.append(locals() ["selection" + str(i) + "_backroom_cost"])
            new_chro_display_cost.append(locals() ["selection" + str(i) + "_display_cost"])
            new_chro_ordering_cost.append(locals() ["selection" + str(i) + "_ordering_cost"])
            new_chro_purchasing_cost.append(locals() ["selection" + str(i) + "_purchasing_cost"])
            new_chro_replenishment.append(locals() ["selection" + str(i) + "_replenishment"])
            new_chro_stockout.append(locals() ["selection" + str(i) + "_stockout"])
            new_chro_lostsales.append(locals() ["selection" + str(i) + "_lostsales"])
            new_chro_quantity_display.append(locals() ["selection" + str(i) + "_qty_displayed"])
            
    # print('new_chro1',new_chro )   
    
    for k in range(tworou):
        selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost,selection1_ordering_cost, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_inventory_cost, selection2_backroom_cost, selection2_display_cost,selection2_ordering_cost, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, max_index, sec_index = selection_pure_rou(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod,chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit)
        selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost,selection1_ordering_cost, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_inventory_cost, selection2_backroom_cost, selection2_display_cost,selection2_ordering_cost, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed = crossover(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod,chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost,selection1_ordering_cost, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new,selection2_inventory_cost, selection2_backroom_cost, selection2_display_cost,selection2_ordering_cost, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend)
        if mode == str(2):
            selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend,selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_sales,selection1_inventory_cost,selection1_backroom_cost,selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_sales,selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost = mutation(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod,chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, CargoLane_ID)
        if mode == str(3):
            selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend,selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_sales,selection1_inventory_cost,selection1_backroom_cost,selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_sales,selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost = mutation(chro, chro_price, chro_sales, chro_profit, chro_new, chro_cargolane_occupied, chro_recommend_prod, chro_inventory_cost, chro_backroom_cost, chro_display_cost, chro_ordering_cost, chro_purchasing_cost, chro_replenishment, chro_stockout, chro_lostsales, chro_quantity_display, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_purchasing_cost, selection1_replenishment, selection1_stockout, selection1_lostsales, selection1_qty_displayed, selection1_inventory_cost, selection1_backroom_cost, selection1_display_cost, selection1_ordering_cost, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_purchasing_cost, selection2_replenishment, selection2_stockout, selection2_lostsales, selection2_qty_displayed, selection2_inventory_cost,selection2_backroom_cost,selection2_display_cost, selection2_ordering_cost, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, CargoLane_ID)
        for i in [1, 2]:
            new_chro.append(locals() ["selection" + str(i)])
            new_chro_price.append(locals() ["selection" + str(i) + "_price"])
            new_chro_sales.append(locals() ["selection" + str(i) + "_sales"])
            new_chro_profit.append(locals() ["selection" + str(i) + "_profit"])
            new_chro_new.append(locals() ["selection" + str(i) + "_new"])
            new_chro_cargolane_occupied.append(locals() ["selection" + str(i) + "_occupied"])
            new_chro_recommend_prod.append(locals() ["selection" + str(i) + "_recommend"])
            new_chro_inventory_cost.append(locals() ["selection" + str(i) + "_inventory_cost"])
            new_chro_backroom_cost.append(locals() ["selection" + str(i) + "_backroom_cost"])
            new_chro_display_cost.append(locals() ["selection" + str(i) + "_display_cost"])
            new_chro_ordering_cost.append(locals() ["selection" + str(i) + "_ordering_cost"])
            new_chro_purchasing_cost.append(locals() ["selection" + str(i) + "_purchasing_cost"])
            new_chro_replenishment.append(locals() ["selection" + str(i) + "_replenishment"])
            new_chro_stockout.append(locals() ["selection" + str(i) + "_stockout"])
            new_chro_lostsales.append(locals() ["selection" + str(i) + "_lostsales"])
            new_chro_quantity_display.append(locals() ["selection" + str(i) + "_qty_displayed"])
    # print('new_chro2',new_chro )   
    
            
    # print(f'new_chro{i}:', new_chro)     
    return new_chro, new_chro_price, new_chro_sales, new_chro_profit, new_chro_new, new_chro_cargolane_occupied, new_chro_recommend_prod, new_chro_inventory_cost, new_chro_backroom_cost, new_chro_display_cost, new_chro_ordering_cost, new_chro_purchasing_cost, new_chro_replenishment, new_chro_stockout, new_chro_lostsales, new_chro_quantity_display

#%%
# main program for the heuristic solution and GA process
def main_program(ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, demand_product_typenum, cargolane_should_empty, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, new_prod_ratio, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, termination):
    if list(set(Product_New)) == [0]:
        sku_min_num = len(list(set(Demand_Product_ID)))
    else:
        sku_min_num = len(list(set(Demand_Product_ID))) + new_prod_ratio
    
    # if mode == str(1):
    #     termination = 20
    # elif mode == str(2):
    #     termination = 200
    # elif mode == str(3):
    #     termination = 200

    if mode == str(1):
        Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, Pro_chro_cargolane_occupied_list, Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display = initial_solution(30, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, Current_Product, Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, mode, setup_cost, replenishment_cost) 
    elif mode == str(2):
        Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, Pro_chro_cargolane_occupied_list, Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display = initial_solution(2*6, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, Current_Product, Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, mode, setup_cost, replenishment_cost) #!!!!!
    elif mode == str(3):
        Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, Pro_chro_cargolane_occupied_list, Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display = initial_solution(30, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, Demand_Product_ID, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, new_prod_ratio, sku_min_num, Current_Product, Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, mode, setup_cost, replenishment_cost)

    # print current profit
    cur_chro, cur_chro_price, cur_chro_sales, cur_chro_profit, cur_chro_new, cur_chro_cargolane_occupied, cur_chro_recommend_prod, cur_chro_cargolane_occupiedlist = current_info(Current_Product, Product_ID, Demand_Product_ID, Product_Price, Demand_Product_Sales, Product_Product_sales, Product_New, Product_Cost, setup_cost, replenishment_cost)
    cur_profit_matrix = pd.DataFrame({"ID": cur_chro, "Profit": cur_chro_profit})
    cur_profit_matrix_without_duplicates = cur_profit_matrix.drop_duplicates(subset = ["ID", "Profit"])
    #cur_each_chro_profit = (sum(cur_profit_matrix_without_duplicates["Profit"]))
    cur_each_chro_profit = (sum(cur_profit_matrix["Profit"]))
    
    iter_times = 1
    iter_maxprofit = [] # 當代最佳
    #iter_maxprofit_oppoloss = [] # 當代最佳的oppo loss
    iter_maxprofit_fitness = [] # 當代最佳的fitness
    
    iter_maxchro = [] # 當代最佳染色體
    iter_maxchro_price = [] # 當代最佳染色體price
    iter_maxchro_sales = []
    iter_maxchro_profit = []
    iter_maxchro_cargolane_occupied = []
    iter_maxchro_recommend_prod = []
    iter_maxchro_inventory_cost=[]
    iter_maxchro_backroom_cost=[]
    iter_maxchro_display_cost=[]
    iter_maxchro_ordering_cost=[]
    iter_maxchro_purchasing_cost=[]
    iter_maxchro_replenishment=[]
    iter_maxchro_stockout=[]
    iter_maxchro_lostsales=[]
    iter_maxchro_quantity_display=[]
    
    
    max_profit_his = [] # 歷代最佳
    #max_profit_min_oppo_his = [] # 歷代最佳
    max_profit_fitness_his = [] # 歷代最佳
    demand=[]
    demand1=[]
    
    it_forchart = []
    iter_cur_profit = []
    iter_heu_profit = []
    
    while iter_times <= termination:
        
        if iter_times == 1:
            each_chro_profit = objective(Pro_chro_profit, Pro_chro, Pro_chro_new, CargoLane_Type, Product_Type, sku_min_num, new_prod_ratio, Pro_chro_price, Pro_chro_cargolane_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, Pro_chro_recommend_prod, Product_New, Pro_chro_cargolane_occupied_list, Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display)
            #objective(chro_profit, chro_ID, chro_new, cargotype, prodtype, num, new_prod_ratio, chro_price, chro_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, chro_recommend, Product_New, chro_cargolane_occupied_list):
            #each_chro_profit, oppo_loss_list, each_chro_profit_withloss = objective(Pro_chro_profit, Pro_chro, Pro_chro_new, CargoLane_Type, Product_Type, sku_min_num, new_prod_ratio, Pro_chro_price, Pro_chro_cargolane_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, Pro_chro_recommend_prod, Product_New, Pro_chro_cargolane_occupied_list)
            #heu_min_indexs = list(locate(each_chro_profit_withloss, lambda x: x == max(each_chro_profit_withloss))) # max profit index們
            heu_min_indexs = list(locate(each_chro_profit, lambda x: x == max(each_chro_profit))) # max profit index們
            heu_min_index = 0
            heu_chro, heu_chro_price, heu_chro_sales, heu_chro_profit, heu_chro_new, heu_chro_cargolane_occupied, heu_chro_recommend_prod, heu_chro_inventory_cost,heu_chro_backroom_cost, heu_chro_display_cost, heu_chro_ordering_cost, heu_chro_purchasing_cost, heu_chro_replenishment, heu_chro_stockout, heu_chro_lostsales, heu_chro_quantity_display = Pro_chro[heu_min_index].copy(), Pro_chro_price[heu_min_index].copy(), Pro_chro_sales[heu_min_index].copy(), Pro_chro_profit[heu_min_index].copy(), Pro_chro_new[heu_min_index].copy(), Pro_chro_cargolane_occupied[heu_min_index].copy(), Pro_chro_recommend_prod[heu_min_index].copy(), Pro_chro_inventory_cost[heu_min_index].copy(), Pro_chro_backroom_cost[heu_min_index].copy(),Pro_chro_display_cost[heu_min_index].copy(),Pro_chro_ordering_cost[heu_min_index].copy(), Pro_chro_purchasing_cost[heu_min_index].copy(), Pro_chro_replenishment[heu_min_index].copy(), Pro_chro_stockout[heu_min_index].copy(), Pro_chro_lostsales[heu_min_index].copy(), Pro_chro_quantity_display[heu_min_index].copy()
            heu_profit_matrix = pd.DataFrame({"ID": heu_chro, "Profit": heu_chro_profit})
            heu_profit_matrix_without_duplicates = heu_profit_matrix.drop_duplicates(subset = ["ID", "Profit"])
            heu_each_chro_profit = each_chro_profit[heu_min_index]
            #heu_each_chro_oppoloss = oppo_loss_list[heu_min_index]
            heu_each_chro_fitness = each_chro_profit[heu_min_index]
            
            heu_result_type = []
            heu_result_capacity = []
            for i in heu_chro:
                if i == "":
                    heu_result_type.append("")
                    heu_result_capacity.append("")
                elif i == "empty":
                    heu_result_type.append("")
                    heu_result_capacity.append("")
                else:
                    heu_result_type.append(Product_Type[Product_ID.index(i)])
                    heu_result_capacity.append(Product_Volume[Product_ID.index(i)])
                    
        if iter_times == 1:
            pass
        else:
            
            Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display = GA(Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display, each_chro_profit) #, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4
            # selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection1_occupied, selection1_recommend, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, selection2_occupied, selection2_recommend, max_index, sec_index = selection(Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, each_chro_profit, oppo_loss_list)
            # Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod = crossover(Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, each_chro_profit, selection1, selection1_price, selection1_sales, selection1_profit, selection1_new, selection2, selection2_price, selection2_sales, selection2_profit, selection2_new, max_index, sec_index, selection1_occupied, selection1_recommend, selection2_occupied, selection2_recommend, each_chro_profit_withloss)
            # if mode == str(2):
            #     Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod = mutation(Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, each_chro_profit, Pro_chro[max_index], Pro_chro_price[max_index], Pro_chro_sales[max_index], Pro_chro_profit[max_index], Pro_chro_new[max_index], Pro_chro[sec_index], Pro_chro_price[sec_index], Pro_chro_sales[sec_index], Pro_chro_profit[sec_index], Pro_chro_new[sec_index], max_index, sec_index, Pro_chro_cargolane_occupied[max_index], Pro_chro_recommend_prod[max_index], Pro_chro_cargolane_occupied[sec_index], Pro_chro_recommend_prod[sec_index], each_chro_profit_withloss, ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4)
            # if mode == str(3):
            #     Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod = mutation(Pro_chro, Pro_chro_price, Pro_chro_sales, Pro_chro_profit, Pro_chro_new, Pro_chro_cargolane_occupied, Pro_chro_recommend_prod, each_chro_profit, Pro_chro[max_index], Pro_chro_price[max_index], Pro_chro_sales[max_index], Pro_chro_profit[max_index], Pro_chro_new[max_index], Pro_chro[sec_index], Pro_chro_price[sec_index], Pro_chro_sales[sec_index], Pro_chro_profit[sec_index], Pro_chro_new[sec_index], max_index, sec_index, Pro_chro_cargolane_occupied[max_index], Pro_chro_recommend_prod[max_index], Pro_chro_cargolane_occupied[sec_index], Pro_chro_recommend_prod[sec_index], each_chro_profit_withloss, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4)
        #each_chro_profit, oppo_loss_list, each_chro_profit_withloss = objective(Pro_chro_profit, Pro_chro, Pro_chro_new, CargoLane_Type, Product_Type, sku_min_num, new_prod_ratio, Pro_chro_price, Pro_chro_cargolane_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, Pro_chro_recommend_prod, Product_New, Pro_chro_cargolane_occupied_list) # 重新確認是否符合限制式
        each_chro_profit = objective(Pro_chro_profit, Pro_chro, Pro_chro_new, CargoLane_Type, Product_Type, sku_min_num, new_prod_ratio, Pro_chro_price, Pro_chro_cargolane_occupied, replenishment_per_time, Demand_Product_ID, Product_max_cargolanenum, CargoLane_Capacity, Pro_chro_recommend_prod, Product_New, Pro_chro_cargolane_occupied_list,Pro_chro_inventory_cost, Pro_chro_backroom_cost, Pro_chro_display_cost, Pro_chro_ordering_cost, Pro_chro_purchasing_cost, Pro_chro_replenishment, Pro_chro_stockout, Pro_chro_lostsales, Pro_chro_quantity_display) # 重新確認是否符合限制式

        # # 以max profit 為選取標準, 再挑選oppo loss 最小的
        # max_position = list(locate(each_chro_profit, lambda x: x == max(each_chro_profit))) # max profit index們
        # last_position = [] # max profit 的機會損失list
        # for i in max_position:
        #     last_position.append(oppo_loss_list[i])
        # best_result = min(last_position) # 最佳獲利中的最小機會損失
        # best_result_index_in_last_position = last_position.index(best_result) # 當代最佳解在last_position&max_position中的index
        # best_result_index = max_position[best_result_index_in_last_position] # 當代最佳解
        
        # iter_maxprofit.append(each_chro_profit[best_result_index]) # 當代最佳放入
        # iter_maxprofit_oppoloss.append(oppo_loss_list[best_result_index])
        # iter_maxprofit_fitness.append(each_chro_profit_withloss[best_result_index])
        
        # iter_maxchro.append(Pro_chro[best_result_index]) # 將當代最佳的各項放入
        # iter_maxchro_price.append(Pro_chro_price[best_result_index])
        # iter_maxchro_sales.append(Pro_chro_sales[best_result_index])
        # iter_maxchro_profit.append(Pro_chro_profit[best_result_index])
        # iter_maxchro_cargolane_occupied.append(Pro_chro_cargolane_occupied[best_result_index])
        # iter_maxchro_recommend_prod.append(Pro_chro_recommend_prod[best_result_index])
        
        # 以max profit - oppo loss 最大為選取標準
        # max_position = list(locate(each_chro_profit_withloss, lambda x: x == max(each_chro_profit_withloss))) # max profit index們
        # last_position = [] # max peach_chro_profit_withloss 的機會損失list
        # for i in max_position:
        #     last_position.append(each_chro_profit[i])
        # best_result = max(last_position) # 最佳獲利中的最小機會損失
        # best_result_index_in_last_position = last_position.index(best_result) # 當代最佳解在last_position&max_position中的index
        # best_result_index = max_position[best_result_index_in_last_position] # 當代最佳解
        
        # index_m = max_position[best_result_index_in_last_position] # 當代最佳解
        #index_m = each_chro_profit_withloss.index(max(each_chro_profit_withloss)) # 當代最佳的index
        
        # a= sum((Pro_chro_profit[3]))
        # b=sum(max(Pro_chro_profit))
        # print(each_chro_profit)
        index_m = each_chro_profit.index(max(each_chro_profit)) # 當代最佳的index
        # print("bawah",each_chro_profit)
        # print("index m", index_m)
        # print()

        iter_maxprofit.append(each_chro_profit[index_m]) # 當代最佳放入
        #iter_maxprofit_oppoloss.append(oppo_loss_list[index_m])
        iter_maxprofit_fitness.append(each_chro_profit[index_m])
        # print("iter_maxprofit_fitness", iter_maxprofit_fitness)
        
        iter_maxchro.append(Pro_chro[index_m]) # 將當代最佳的各項放入
        iter_maxchro_price.append(Pro_chro_price[index_m])
        iter_maxchro_sales.append(Pro_chro_sales[index_m])
        iter_maxchro_profit.append(Pro_chro_profit[index_m])
        iter_maxchro_cargolane_occupied.append(Pro_chro_cargolane_occupied[index_m])
        iter_maxchro_recommend_prod.append(Pro_chro_recommend_prod[index_m])
        # print(iter_maxchro_sales)
        
        iter_maxchro_inventory_cost.append(Pro_chro_inventory_cost[index_m])
        iter_maxchro_backroom_cost.append(Pro_chro_backroom_cost[index_m])
        iter_maxchro_display_cost.append(Pro_chro_display_cost[index_m])
        iter_maxchro_ordering_cost.append(Pro_chro_ordering_cost[index_m])
        iter_maxchro_purchasing_cost.append(Pro_chro_purchasing_cost[index_m])
        iter_maxchro_replenishment.append(Pro_chro_replenishment[index_m])
        iter_maxchro_stockout.append(Pro_chro_stockout[index_m])
        iter_maxchro_lostsales.append(Pro_chro_lostsales[index_m])
        iter_maxchro_quantity_display.append(Pro_chro_quantity_display[index_m])
        # print("Pro_chro[index_m]", Pro_chro[index_m])
        # print("iter_maxchro_stockout", Pro_chro_stockout[index_m])
        # print("iter_maxchro_lostsales", Pro_chro_lostsales[index_m])
        
        max_profit_his.append(iter_maxprofit[iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))])
        #max_profit_min_oppo_his.append(iter_maxprofit_oppoloss[iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))])
        max_profit_fitness_his.append(iter_maxprofit_fitness[iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))])
        
        
        iter_cur_profit.append(cur_each_chro_profit)
        iter_heu_profit.append(heu_each_chro_profit)
        
        it_forchart.append(iter_times)
        
        max_rec=[]
        max_chro= iter_maxchro[iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))]
        for i in range(len(iter_maxchro_cargolane_occupied[0])):
            idx= iter_maxchro_cargolane_occupied[0][i]-1
            max_rec.append(max_chro[idx])
        iter_maxchro_recommend_prod[iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))]= max_rec
        
        iter_times += 1
        
    result_type = []
    result_capacity = []
    for i in iter_maxchro[iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))]:
        if i == "":
            result_type.append("")
            result_capacity.append("")
        elif i == "empty":
            result_type.append("")
            result_capacity.append("")
        else:
            result_type.append(Product_Type[Product_ID.index(i)])
            result_capacity.append(Product_Volume[Product_ID.index(i)])
            
    # CargoLane_Type 還原
    copy_cargolane_type = CargoLane_Type.copy()
    for i in range(len(copy_cargolane_type)):
        if type(copy_cargolane_type[i]) == str:
            copy_cargolane_type[i] = int(copy_cargolane_type[i][1])
        else:
            copy_cargolane_type[i] = int(copy_cargolane_type[i])
        
    ##### print AI解
    if mode ==  "1": # print the AI result: mode 1
        index_1 = iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))
        costlist = []
        for i in range(len(iter_maxchro[index_1])):
            if iter_maxchro[index_1][i] == "" or iter_maxchro[index_1][i] == "empty":
                costlist.append(0)
            else:
                costlist.append(Product_Cost[Product_ID.index(iter_maxchro[index_1][i])])
        final_result = {"VM ID": VM_ID, "Device ID": CargoLane_Device_ID, "Site ID": CargoLane_Site_ID, "CargoLane ID": CargoLane_ID, "Product selection": iter_maxchro[index_1], "Product price": iter_maxchro_price[index_1], "Product cost": costlist, "Product sales": iter_maxchro_sales[index_1], "Product profit": iter_maxchro_profit[index_1], "cargo_type": copy_cargolane_type, "prod_type": result_type, "prod_vol": result_capacity, "Inventory_cost": iter_maxchro_inventory_cost[index_1],  "Backroom_cost": iter_maxchro_backroom_cost[index_1],  "Display_cost": iter_maxchro_display_cost[index_1],  "Ordering_cost": iter_maxchro_ordering_cost[index_1]}
        output_final_result = pd.DataFrame(final_result)
        output_final_summarization = pd.DataFrame()
        output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit[index_1], "Value_type": "revenue"}, ignore_index=True)
        #output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit_oppoloss[index_1], "Value_type": "opportunity loss"}, ignore_index=True)
        output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit_fitness[index_1], "Value_type": "fitness"}, ignore_index=True)
        for i in range(len(iter_maxchro_cargolane_occupied[index_1])):
            output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxchro_cargolane_occupied[index_1][i], "Value_type": "empty"}, ignore_index=True)
        print(output_final_summarization)
        
        #!!!!!
    if mode == str(2): # print the AI result: mode 2
        index_2 = iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))
        costlist = []
        for i in range(len(iter_maxchro[index_2])):
            if iter_maxchro[index_2][i] == "" or iter_maxchro[index_2][i] == "empty":
                costlist.append(0)
            else:
                costlist.append(Product_Cost[Product_ID.index(iter_maxchro[index_2][i])])

        final_result = {"VM ID": VM_ID, "Device ID": CargoLane_Device_ID, "Site_ID": CargoLane_Site_ID, "CargoLane ID": CargoLane_ID, "Product selection": iter_maxchro[index_2], "Product price": iter_maxchro_price[index_2], "Purchasing cost": iter_maxchro_purchasing_cost[index_2], "Product sales": iter_maxchro_sales[index_2], "Product profit": iter_maxchro_profit[index_2], "Cargo_type": copy_cargolane_type, "Prod_type": result_type, "Prod_vol": result_capacity, "Inventory_cost": iter_maxchro_inventory_cost[index_2],  "Backroom_cost": iter_maxchro_backroom_cost[index_2],  "Display_cost": iter_maxchro_display_cost[index_2],  "Ordering_cost": iter_maxchro_ordering_cost[index_2], "Replenishment": iter_maxchro_replenishment[index_2], "Stockout": iter_maxchro_stockout[index_2], "Lostsales": iter_maxchro_lostsales[index_2], "Quantity display": iter_maxchro_quantity_display[index_2]}
        output_final_result = pd.DataFrame(final_result)
        output_final_summarization = pd.DataFrame()
        output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit[index_2], "Value_type": "revenue"}, ignore_index=True)
        #output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit_oppoloss[index_2], "Value_type": "opportunity loss"}, ignore_index=True)
        output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit_fitness[index_2], "Value_type": "fitness"}, ignore_index=True)
        for i in range(len(iter_maxchro_cargolane_occupied[index_2])):
            output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxchro_cargolane_occupied[index_2][i], "Value_type": "empty"}, ignore_index=True)
            # print(output_final_summarization)
        for j in range(len(iter_maxchro_recommend_prod[index_2])):
            output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxchro_recommend_prod[index_2][j], "Value_type": "recommend"}, ignore_index=True)
        # print(output_final_summarization) #!!!!!
        # print("Fitness GA", iter_maxprofit_fitness[index_2])
        # data_collect={"Fitness_each_GA": iter_maxprofit_fitness[index_2]}
        #data_fitness_GA_csv={"Fitness_GA":max_profit_fitness_his, "Oppo_loss":iter_maxprofit_oppoloss[index_2]}
        data_fitness_GA_csv={"Fitness_GA":max_profit_fitness_his}

        fitness_GA_csv = pd.DataFrame(data_fitness_GA_csv)
        demand.append(iter_maxchro_sales[index_2])
        # print(demand)
        demand1.append(sum(demand[0]))
        #print('##')
        
    if mode == "3": # print the AI result: mode 3
        index_3 = iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))
        costlist = []
        for i in range(len(iter_maxchro[index_3])):
            if iter_maxchro[index_3][i] == "" or iter_maxchro[index_3][i] == "empty":
                costlist.append(0)
            else:
                costlist.append(Product_Cost[Product_ID.index(iter_maxchro[index_3][i])])
        final_result = {"VM ID": VM_ID, "Device ID": CargoLane_Device_ID, "Site_ID": CargoLane_Site_ID, "CargoLane ID": CargoLane_ID, "Product selection": iter_maxchro[index_3], "Product price": iter_maxchro_price[index_3], "Product cost": costlist, "Product sales": iter_maxchro_sales[index_3], "Product profit": iter_maxchro_profit[index_3], "cargo_type": copy_cargolane_type, "prod_type": result_type, "prod_vol": result_capacity, "Inventory_cost": iter_maxchro_inventory_cost[index_3],  "Backroom_cost": iter_maxchro_backroom_cost[index_3],  "Display_cost": iter_maxchro_display_cost[index_3],  "Ordering_cost": iter_maxchro_ordering_cost[index_3]}
        output_final_result = pd.DataFrame(final_result)
        output_final_summarization = pd.DataFrame()
        output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit[index_3], "Value_type": "revenue"}, ignore_index=True)
        #output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit_oppoloss[index_3], "Value_type": "opportunity loss"}, ignore_index=True)
        output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxprofit_fitness[index_3], "Value_type": "fitness"}, ignore_index=True)
        for i in range(len(iter_maxchro_cargolane_occupied[index_3])):
            output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxchro_cargolane_occupied[index_3][i], "Value_type": "empty"}, ignore_index=True)
        # for j in range(len(recommend_prod)):
        #     output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "value": recommend_prod[j], "Value_type": "recommend"}, ignore_index=True)
        for j in range(len(iter_maxchro_recommend_prod[index_3])):
            output_final_summarization = output_final_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": iter_maxchro_recommend_prod[index_3][j], "Value_type": "recommend"}, ignore_index=True)
        print(output_final_summarization)
        print('##')
        
    ##### print啟發解
    if mode ==  "1": # print the heuristic result: mode 1
        costlist_h = []
        for i in range(len(heu_chro)):
            if heu_chro[i] == "" or heu_chro[i] == "empty":
                costlist_h.append(0)
            else:
                costlist_h.append(Product_Cost[Product_ID.index(heu_chro[i])])
        heuristic_result = {"VM ID": VM_ID, "Device ID": CargoLane_Device_ID, "Site ID": CargoLane_Site_ID, "CargoLane ID": CargoLane_ID, "Product selection": heu_chro, "Product price": heu_chro_price, "Purchasing cost": costlist_h, "Product sales": heu_chro_sales, "Product profit": heu_chro_profit, "cargo_type": copy_cargolane_type, "prod_type": heu_result_type, "prod_vol": heu_result_capacity,  "Inventory_cost": heu_chro_inventory_cost,  "Backroom_cost": heu_chro_backroom_cost,  "Display_cost": heu_chro_display_cost,  "Ordering_cost": heu_chro_ordering_cost}
        output_heuristic_result = pd.DataFrame(heuristic_result)
        output_heuristic_summarization = pd.DataFrame()
        output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_profit, "Value_type": "revenue"}, ignore_index=True)
        #output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_oppoloss, "Value_type": "opportunity loss"}, ignore_index=True)
        output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_fitness, "Value_type": "fitness"}, ignore_index=True)
        for i in range(len(heu_chro_cargolane_occupied)):
            output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_chro_cargolane_occupied[i], "Value_type": "empty"}, ignore_index=True)
        print(output_heuristic_summarization)
        
        
    if mode == str(2): # print the heuristic result: mode 2
        costlist_h = []
        for i in range(len(heu_chro)):
            if heu_chro[i] == "" or heu_chro[i] == "empty":
                costlist_h.append(0)
            else:
                costlist_h.append(Product_Cost[Product_ID.index(heu_chro[i])])
        heuristic_result = {"VM ID": VM_ID, "Device ID": CargoLane_Device_ID, "Site_ID": CargoLane_Site_ID, "CargoLane ID": CargoLane_ID, "Product selection": heu_chro, "Product price": heu_chro_price, "Purchasing cost": costlist_h, "Product sales": heu_chro_sales, "Product profit": heu_chro_profit, "cargo_type": copy_cargolane_type, "prod_type": heu_result_type, "prod_vol": heu_result_capacity, "Inventory_cost": heu_chro_inventory_cost,  "Backroom_cost": heu_chro_backroom_cost,  "Display_cost": heu_chro_display_cost,  "Ordering_cost": heu_chro_ordering_cost}
        output_heuristic_result = pd.DataFrame(heuristic_result)
        output_heuristic_summarization = pd.DataFrame()
        output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_profit, "Value_type": "revenue"}, ignore_index=True)
        #output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_oppoloss, "Value_type": "opportunity loss"}, ignore_index=True)
        output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_fitness, "Value_type": "fitness"}, ignore_index=True)
        for i in range(len(heu_chro_cargolane_occupied)):
            output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_chro_cargolane_occupied[i], "Value_type": "empty"}, ignore_index=True)
        for j in range(len(heu_chro_cargolane_occupied)):
            output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_chro_recommend_prod[j], "Value_type": "recommend"}, ignore_index=True)
        #print(output_heuristic_summarization)
        
        
    if mode == "3": # print the heuristic result: mode 3
        costlist_h = []
        for i in range(len(heu_chro)):
            if heu_chro[i] == "" or heu_chro[i] == "empty":
                costlist_h.append(0)
            else:
                costlist_h.append(Product_Cost[Product_ID.index(heu_chro[i])])
        heuristic_result = {"VM ID": VM_ID, "Device ID": CargoLane_Device_ID, "Site_ID": CargoLane_Site_ID, "CargoLane ID": CargoLane_ID, "Product selection": heu_chro, "Product price": heu_chro_price, "Purchasing cost": costlist_h, "Product sales": heu_chro_sales, "Product profit": heu_chro_profit, "cargo_type": copy_cargolane_type, "prod_type": heu_result_type, "prod_vol": heu_result_capacity, "Inventory_cost": heu_chro_inventory_cost,  "Backroom_cost": heu_chro_backroom_cost,  "Display_cost": heu_chro_display_cost,  "Ordering_cost": heu_chro_ordering_cost}
        output_heuristic_result = pd.DataFrame(heuristic_result)
        output_heuristic_summarization = pd.DataFrame()
        output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_profit, "Value_type": "revenue"}, ignore_index=True)
        #output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_oppoloss, "Value_type": "opportunity loss"}, ignore_index=True)
        output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_each_chro_fitness, "Value_type": "fitness"}, ignore_index=True)
        for i in range(len(heu_chro_cargolane_occupied)):
            output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_chro_cargolane_occupied[i], "Value_type": "empty"}, ignore_index=True)
        for j in range(len(heu_chro_cargolane_occupied)):
            output_heuristic_summarization = output_heuristic_summarization.append({"Site ID": CargoLane_Site_ID[0], "Device ID": CargoLane_Device_ID[0], "Value": heu_chro_recommend_prod[j], "Value_type": "recommend"}, ignore_index=True)
        print(output_heuristic_summarization)
        
    #####

    #print(max(max_profit_his))
    #print(max_profit_his)
    #print(max_profit_fitness_his)
    
    
    # history diagram
    
    # plt.figure()
    # plt.title("GA history" + " " + file) # title
    # plt.plot(it_forchart, max_profit_fitness_his, label = "AI profit= " + str(round(max(max_profit_fitness_his), 2)))
    # #plt.plot(it_forchart, iter_cur_profit, label = "current profit= " + str(round(cur_each_chro_profit, 2)))
    # #plt.plot(it_forchart, iter_heu_profit, label = "heuristic profit= " + str(round(heu_each_chro_profit, 2)))
    # plt.xlabel('iterations')
    # plt.ylabel('max profit')
    # #plt.ylim(round((cur_each_chro_profit - 200) / 100, 0) * 100, round((round(max(max_profit_fitness_his), 0) + 400) / 100, 0) * 100)
    # plt.legend()
    # plt.show()
    # # history diagram
    # plt.figure()
    # plt.title("oppotunity loss history") # title
    # plt.plot(it_forchart, max_profit_min_oppo_his, label = "oppo loss of max profit= " + str(round(max(max_profit_min_oppo_his), 2)))   # blue line without marker
    # plt.xlabel('iterations')
    # plt.ylabel('oppo loss of max profit')
    # plt.ylim(round((min(max_profit_min_oppo_his) - 50) / 100, 0) * 100, round((round(max(max_profit_min_oppo_his), 0) + 50) / 100, 0) * 100)
    # plt.legend()
    # plt.show()
    
    
    # print("heu:", heu_each_chro_fitness, "AI:", iter_maxprofit_fitness[iter_maxprofit_fitness.index(max(iter_maxprofit_fitness))])
    return output_final_result, output_final_summarization, cur_each_chro_profit, heu_each_chro_profit, output_heuristic_result, output_heuristic_summarization, fitness_GA_csv, max_profit_fitness_his, demand1

#%%
# read the in/output path, parameters setting, error log
# time_start = time.time() # start to count the time 開始計時
# parameters setting
mode = str(2)
new_prod_ratio = int(1) # 5%

# inputpath = os.path.normpath(sys.argv[1])
# outputpath = os.path.normpath(sys.argv[2])
# termination = int(os.path.normpath(sys.argv[3]))

# for heuristic
# if mode == str(1):
#     termination = 2
# elif mode == str(2):
#     termination = 2
# elif mode == str(3):
#     termination = 2

if mode == str(1):
    termination = 20
elif mode == str(2):
    termination = 75
elif mode == str(3):
    termination = 200
    


inputpath = r"C:\Users\Admin\iCloudDrive\KULYEAH\lab\naskah\Thesis\ruun" # test
if mode == str(1):
    outputpath = "/Users/nataliafebri/Documents/Lab Meeting/Lab Meeting Rabu/Project VM/31 Oct/Mode1" # test
elif mode == str(2):
    outputpath = r"C:\Users\Admin\iCloudDrive\KULYEAH\lab\naskah\Thesis\ruuntest\tes"  # !!!!!
    outputpath_comparison= r"C:\Users\Admin\iCloudDrive\KULYEAH\lab\naskah\Thesis\ruuntest\tes"
else:
    outputpath =r"C:\Users\Admin\iCloudDrive\KULYEAH\lab\naskah\Thesis\GAnew"  # test

# for heuristic
# iter_mode1 = mode == str(1) and termination == 1
# iter_mode2 = mode == str(2) and termination == 1
# iter_mode3 = mode == str(3) and termination == 1
# iter_def = iter_mode1 == True or iter_mode2 == True or iter_mode3 == True

#iter_mode1 = mode == str(1) and 20 <= termination <= 600
#iter_mode2 = mode == str(2) and 200 <= termination <= 600
#iter_mode3 = mode == str(3) and 200 <= termination <= 600
#iter_def = iter_mode1 == True or iter_mode2 == True or iter_mode3 == True
iter_def = True

today_std = datetime.date.today()
today_std = str(today_std.year * 10000 + today_std.month * 100 + today_std.day)

today_std_time = time.localtime()
today_std_time = time.strftime('%H%M%S', today_std_time)

today_std_for_property = datetime.date.today()
today_std_for_property = int(today_std_for_property.year * 10000 + today_std_for_property.month * 100 + today_std_for_property.day)

#now we will Create and configure logger 
if mode == str(1):
    logging.basicConfig(filename="std_mode1_" + today_std + today_std_time + ".log", format='%(asctime)s %(message)s', filemode='w')
elif mode == str(2):
    logging.basicConfig(filename="std_mode2_" + today_std + today_std_time + ".log", format='%(asctime)s %(message)s', filemode='w')
elif mode == str(3):
    logging.basicConfig(filename="std_mode3_" + today_std + today_std_time + ".log", format='%(asctime)s %(message)s', filemode='w')

#Let us Create an object 
logger=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

ok = 0
okno = 0
okno_list = []

print("This program is a property of National Taiwan University of Science and Technology." + "\n")
logger.info("This program is a property of National Taiwan University of Science and Technology." + "\n")
exe_times=[]
exe=[]
fitness=[]
fitness_each=[]
demands=[]
demand_each=[]
if os.path.exists(inputpath) and os.path.exists(outputpath) and today_std_for_property <= 20231231 and iter_def == True:
    inputfile_list = os.listdir(inputpath)
    for file in inputfile_list:
        # try:
            time_start = time.time()
            
            
            print(file)
            logger.info(file)
            
            input_excel = os.path.join(inputpath, file)
            input_sheet_VM = "VM_info"
            input_sheet_ProEast = "Product_info_東區"
            input_sheet_ProNotEast = "Product_info_非東區"
            df_VM_info = pd.read_excel(input_excel, sheet_name = input_sheet_VM) # input VM_info sheet
            
            cargolane_num_should_be = (df_VM_info["CargoLane_TotalNumber"].squeeze()).tolist()
            
            df_VM_info = df_VM_info.append({"CargoLane_TotalNumber": int(0)}, ignore_index = True)
            CargoLane_Site_ID_for_log = int((df_VM_info.loc[0, ["Site_ID"]].squeeze()))
            
            if type(df_VM_info["CargoLane_ID"].squeeze().tolist()) == float:
                if math.isnan((df_VM_info["CargoLane_ID"].squeeze()).tolist()) == True:
                    print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:VM_info is empty" + "\n")
                    logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:VM_info is empty" + "\n")
                    continue
            
            CargoLane_TotalNumber_first = int(df_VM_info.at[0, "CargoLane_TotalNumber"])
            if len(cargolane_num_should_be) != CargoLane_TotalNumber_first:
                print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:The number of Cargolanes is not same as CargoLane_TotalNumber" + "\n")
                logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:The number of Cargolanes is not same as CargoLane_TotalNumber" + "\n")
            #     continue
                
            locate_ID = list(OrderedDict.fromkeys((df_VM_info.loc[:, "Device_ID"].squeeze()).tolist())) # 重複值刪除，顯示所有點位
            del locate_ID[-1]
            Index_strart = int(0)
            Index_end = int(df_VM_info.at[0, "CargoLane_TotalNumber"]) - 1
            # Index_end = max((df_VM_info["CargoLane_ID"].squeeze()).tolist()) - 1 # 直接抓最後一個ID - 1
            # Index_end = len((df_VM_info["CargoLane_ID"].squeeze()).tolist()) - 2
            
            today = datetime.date.today()
            today = str(today.year * 10000 + today.month * 100 + today.day)
                    
            input_sheet_ProDemand = "Product_demand"
                # print(Index_strart, ":", Index_end)
            
            df_VM_info, df_Product_info, df_Product_demand, df_replacement_matrix, VM_ID, CargoLane_Device_ID, CargoLane_Site_ID, CargoLane_TotalNumber, CargoLane_ID, CargoLane_Type, CargoLane_Height_Max, CargoLane_Height_Min, CargoLane_Diameter_Max_1, CargoLane_Diameter_Min_1, CargoLane_Area, CargoLane_Capacity, Current_Product, Max_Prod_Cnt, Min_Prod_Cnt, CargoLane_Allow_Special, CargoLane_Average_Replenishment, CargoLane_Category_Rate, CargoLane_Brand_Rate, Product_ID, Product_Price, Product_Cost, Product_Product_sales, Product_Type, Product_Volume, Product_Length, Product_Width, Product_Height, Product_New, Product_Brand, Product_Category, Product_Specialsize, Demand_Product_ID, Demand_Product_Sales, replacement_matrix, Demand_zero = read_data(df_VM_info, input_excel, input_sheet_ProEast, input_sheet_ProNotEast, input_sheet_ProDemand, Index_strart, Index_end)

            check_demand_prod_in_prodlist = 0
            for i in Demand_Product_ID:
                if i not in Product_ID:
                    check_demand_prod_in_prodlist += 1
            if check_demand_prod_in_prodlist > 0:
                print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Some products in Product_demand are not in Product_info" + "\n")
                logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Some products in Product_demand are not in Product_info" + "\n")
                continue
        
            if (type(CargoLane_Average_Replenishment[0]) == int and CargoLane_Average_Replenishment[0] > 0) or (type(CargoLane_Average_Replenishment[0]) == float and CargoLane_Average_Replenishment[0] > 0):
                pass
            else:
                print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Average Replenishment" + "\n")
                logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Average Replenishment" + "\n")
            #     continue
            
            ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, demand_product_typenum, cargolane_should_empty, cargolane_type_num, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, product_product_typenum, replenishment_per_time, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, Cost_CargoLane1, Cost_CargoLane2, Cost_CargoLane3, Cost_CargoLane4, Cost_CargoLane5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, setup_cost, replenishment_cost, unit_inventory_cost,unit_backroom_cost,unit_display_cost,unit_ordering_cost = classify_demand_product(Product_ID, Product_Type, Product_Volume, Product_Price, Demand_Product_ID, Demand_Product_Sales, CargoLane_Average_Replenishment, Product_New, Product_Brand, Product_Specialsize, Product_Cost)
            Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, Recommend_cost1, Recommend_cost2, Recommend_cost3, Recommend_cost4, Recommend_cost5, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4 = classify_recommend_product(Product_ID, Product_Type, Product_Volume, Product_Price, Demand_Product_ID, Product_Cost, setup_cost, replenishment_cost)
            
            # # 現況解跟Demand_Product品項不符, CargoLane_TotalNumber不等於CargoLane_ID, 新品與互斥品原則
            # check_current_prod = list(set(Current_Product))
            # while np.nan in check_current_prod:
            #     check_current_prod.remove(np.nan)
            # check_Demand_Product_ID = Demand_Product_ID.copy()
            # for i in range(len(check_current_prod)):
            #     if type(check_current_prod[i]) != str:
            #         if math.isnan(check_current_prod[i]) == True:
            #             check_current_prod[i] = -1
            # while -1 in check_current_prod:
            #     check_current_prod.remove(-1)
            # check_current_prod.sort()
            # check_Demand_Product_ID.sort()
            
            # if check_current_prod != check_Demand_Product_ID:
            #     print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Current_Product are not same as Demand_Product" + "\n")
            #     logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Current_Product are not same as Demand_Product" + "\n")
            #     continue
            
            # check_replace = 0
            # for i in check_current_prod:
            #     if i in replacement_matrix.keys():    
            #         if replacement_matrix[i] in check_current_prod:
            #             check_replace += 1
            # if check_replace != 0:
            #     print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Current_Product has conflict between product and product" + "\n")
            #     logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:Current_Product has conflict between product and product" + "\n")
            #     continue
            
            # check_special_ornot = 0
            # for i in range(len(Product_Specialsize)):
            #     for j in Demand_Product_ID:
            #         if Product_Specialsize[Product_ID.index(j)] == 1:
            #             check_special_ornot += 1
            
            # if (list(set(Product_New)) != [0] and new_prod_ratio + len(list(set(Demand_Product_ID))) > CargoLane_TotalNumber) \
            #     or (list(set(Product_New)) == [0] and len(list(set(Demand_Product_ID))) > CargoLane_TotalNumber) \
            #     or (1 not in list(set(CargoLane_Allow_Special)) and check_special_ornot > 0):
            #     print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:CargoLanes are not sufficient" + "\n")
            #     logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:CargoLanes are not sufficient" + "\n")
            #     continue
            
            # if len(ID_CargoLane2) - len(ID_CargoLane1) > cargolane_type_num[2] + cargolane_type_num[7] or len(ID_CargoLane4) - len(ID_CargoLane3) > cargolane_type_num[4] + cargolane_type_num[5] + cargolane_type_num[9]:
            #     print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:CargoLanes are not sufficient(II)" + "\n")
            #     logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution failed:CargoLanes are not sufficient(II)" + "\n")
            #     continue
        
            print("Model is running...")
            logger.info("Model is running...")
            
            output_final_result, output_final_summarization, cur_each_chro_profit, heu_each_chro_profit, output_heuristic_result, output_heuristic_summarization, fitness_GA_csv, max_profit_fitness_his, demand1 = main_program(ID_CargoLane1, ID_CargoLane2, ID_CargoLane3, ID_CargoLane4, ID_CargoLane5, Price_CargoLane1, Price_CargoLane2, Price_CargoLane3, Price_CargoLane4, Price_CargoLane5, Sales_CargoLane1, Sales_CargoLane2, Sales_CargoLane3, Sales_CargoLane4, Sales_CargoLane5, Product_max_cargolanenum, demand_product_typenum, cargolane_should_empty, New_ID1, New_ID2, New_ID3, New_ID4, New_ID5, Brand_CargoLane1, Brand_CargoLane2, Brand_CargoLane3, Brand_CargoLane4, Brand_CargoLane5, Recommend_ID1, Recommend_ID2, Recommend_ID3, Recommend_ID4, Recommend_ID5, Recommend_price1, Recommend_price2, Recommend_price3, Recommend_price4, Recommend_price5, new_prod_ratio, replacement_matrix, New_profit1, New_profit2, New_profit3, New_profit4, New_profit5, sID_CargoLane1, sID_CargoLane2, sID_CargoLane3, sID_CargoLane4, sPrice_CargoLane1, sPrice_CargoLane2, sPrice_CargoLane3, sPrice_CargoLane4, sSales_CargoLane1, sSales_CargoLane2, sSales_CargoLane3, sSales_CargoLane4, sCost_CargoLane1, sCost_CargoLane2, sCost_CargoLane3, sCost_CargoLane4, sNew_ID1, sNew_ID2, sNew_ID3, sNew_ID4, sNew_profit1, sNew_profit2, sNew_profit3, sNew_profit4, sRecommend_ID1, sRecommend_ID2, sRecommend_ID3, sRecommend_ID4, sRecommend_price1, sRecommend_price2, sRecommend_price3, sRecommend_price4, sRecommend_cost1, sRecommend_cost2, sRecommend_cost3, sRecommend_cost4, snID_CargoLane1, snID_CargoLane2, snID_CargoLane3, snID_CargoLane4, snPrice_CargoLane1, snPrice_CargoLane2, snPrice_CargoLane3, snPrice_CargoLane4, snSales_CargoLane1, snSales_CargoLane2, snSales_CargoLane3, snSales_CargoLane4, snCost_CargoLane1, snCost_CargoLane2, snCost_CargoLane3, snCost_CargoLane4, snNew_ID1, snNew_ID2, snNew_ID3, snNew_ID4, snNew_profit1, snNew_profit2, snNew_profit3, snNew_profit4, snRecommend_ID1, snRecommend_ID2, snRecommend_ID3, snRecommend_ID4, snRecommend_price1, snRecommend_price2, snRecommend_price3, snRecommend_price4, snRecommend_cost1, snRecommend_cost2, snRecommend_cost3, snRecommend_cost4, termination)
            
            outputpath_s = os.path.join(outputpath, today + '_' + file + "_" + mode + "_result2.csv") # 設定路徑及檔名
            outputpath_r = os.path.join(outputpath, today + '_' + file + "_" + mode + "_result1.csv") # 設定路徑及檔名
            output_final_result.to_csv(outputpath_r, sep = ",", index = False, encoding = "utf-8")
            output_final_summarization.to_csv(outputpath_s, sep = ",", header = False, index = False, encoding = "utf-8")
            
            # output 啟發解
            outputpath_s_h = os.path.join(outputpath, "heuristic_" + file + "_" + mode + "_result2.csv") # 設定路徑及檔名
            outputpath_r_h = os.path.join(outputpath, "heuristic_" + file + "_" + mode + "_result1.csv") # 設定路徑及檔名
            output_heuristic_result.to_csv(outputpath_r_h, sep = ",", index = False, encoding = "utf-8")
            output_heuristic_summarization.to_csv(outputpath_s_h, sep = ",", header = False, index = False, encoding = "utf-8")
            
            
            outputpath_graph = os.path.join(outputpath_comparison, "Fitness" + file + "_" + mode + "GA.csv") # 設定路徑及檔名
            fitness_GA_csv.to_csv(outputpath_graph, sep = ",", index = False, encoding = "utf-8")
            
            demands.append(sum(demand1))
            demand_each.append(demands)
            
            fitness.append(max(max_profit_fitness_his))
            fitness_each.append(fitness)
                        
            
            # Index_strart = Index_end + 1
            CargoLane_Quantity = int(df_VM_info.at[Index_strart, "CargoLane_TotalNumber"])
            # Index_end = Index_strart + CargoLane_Quantity - 1
            print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution succeed" + "\n")
            logger.info("result:" + str(CargoLane_Site_ID_for_log) + ":Execution succeed" + "\n")
            time_end = time.time()    # 結束計時
            time_total = time_end - time_start    # 執行所花時間
            exe.append(time_total)
            exe_times.append(exe)
            print('Spend:', exe, '(s)')
            
            if heu_each_chro_profit > 1:
                ok += 1
            else:
                okno += 1
                okno_list.append(file[20:])
                
        # except:                   # 如果 try 的內容發生錯誤，就執行 except 裡的內容
            print("result:" + str(CargoLane_Site_ID_for_log) + ":Execution succeed" + "\n")
            logger.error("result:" + str(CargoLane_Site_ID_for_log) + ":Execution succeed" + "\n")
    filename = "execution_times.csv"
    save_directory = outputpath  # Specify the directory where the CSV file should be saved
    fullpath = os.path.join(save_directory, filename)
    outputfitness = os.path.join(outputpath_comparison, "Fitness_each.csv")
    outputdemand = os.path.join(outputpath_comparison, "demand_each.csv")


    with open(fullpath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Execution Time'])

        for i in range(len(inputfile_list)):
            if i < len(exe_times):  # Check if the index is within the range of exe_times
                writer.writerow([inputfile_list[i], exe[i]])
                
    with open(outputfitness, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Fitness'])
        
        for i in range(len(inputfile_list)):
            if i < len(fitness_each):
                writer.writerow([inputfile_list[i], fitness[i]])
                
    with open(outputdemand, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Demand'])
        
        for i in range(len(inputfile_list)):
            if i < len(demand_each):
                writer.writerow([inputfile_list[i], demands[i]])
            
            # pass                  # 略過
            # exe_times.append(exe)
            # print("tes", exe_times)
else:
    if today_std_for_property > 20231231:
        print("The deadline of exection was met, it's exceeded 20231231")
    elif iter_def == False:
        print("The number of iteration is out of range")
    elif os.path.exists(inputpath) == False and os.path.exists(outputpath) == False:
        print(inputpath, "and", outputpath, "do not exist")
    elif os.path.exists(inputpath) == False:
        print(inputpath, "do not exist")
    elif os.path.exists(outputpath) == False:
        print(outputpath, "do not exist")
        
# print(fitness_each)
avgfit = sum(fitness_each[-1]) / len(fitness_each[-1])
avgtime = sum(exe_times[-1]) / len(exe_times[-1])
maxfit = max(fitness_each[-1])
maxtime = max(exe_times[-1])

filename = "average_result.csv"
save_directory = outputpath  # Specify the directory where the CSV file should be saved
fullpath = os.path.join(save_directory, filename)
data = {'Average fitness': [avgfit] , 'Max fitness': [maxfit],'Average times': [avgtime], 'Max times': [maxtime]}
df = pd.DataFrame(data)

path = os.path.join(save_directory, filename)
df.to_csv(path, index=False) 

    
for i in range(5):
    win32api.Beep(random.randint(500,1000), random.randint(750,3000))
    

    
# @email_sender(recipient_emails=["rafih17@gmail.com"], sender_email="rafih46@gmail.com")
# def main():
#     even_arr = []
#     for i in range(10000):
#         if i%2==0:
#             even_arr.append(i)

# if __name__=='__main__':
#     main()
# exe_times.append(exe)
# print(exe_times)
        

# filename = "execution_times.csv"
# save_directory = r"C:\Users\Admin\iCloudDrive\KULYEAH\lab\naskah\Thesis\GA(3,2)"
# fullpath = os.path.join(save_directory, filename)
# with open(fullpath, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['File', 'Execution Time'])
    
#     for i in range(len(inputfile_list)):
#         writer.writerow([inputfile_list[i], exe[i]])
# print("Execution times exported to execution_times.csv")


# time_end = time.time()    # 結束計時
# time_total = time_end - time_start    # 執行所花時間
# print('Spend:', time_total, '(s)')

# error log priority
# VM_info is empty v
# The number of Cargolanes is not same as CargoLane_TotalNumber v
# Some products in Product_demand are not in Product_info v
# Average Replenishment v
# Current_Product are not same as Demand_Product 
# Current_Product has conflict between product and product v
# CargoLanes are not sufficient v
# Incorrect input data, execution failed v


#%%
# to do list and need to check/revise
# 1. 啟發解還是有可能不符合品項數限制式
# 2. 最大 單位利潤*銷量/貨道需求!!!!! 只適用mode2推薦品項? 因為一般選品是用隨機, 新品及mode3推薦品沒有貨道可以計算 (O)

# 4. in/output path 輸入 (O)
# 5. 貨道尺寸選擇
# 6. 新品來源調整 (O)
# 7. 輸入輸出檔名調整site_id_device_id (O)

# 8. Heuristic加入一組max選解 (O)
# 9. current加入population (O)
# 10. 推薦品項利潤算法 (O)
# 11. SIZE版本: mutation要改candidate2 跟index
# 12. SIZE版本: chromosome要改cargoID 跟CargoLane_ID要改int
# 13. SIZE: chro_occupied要改
# 14. SIZE: objective要改


# 
# min_sku有問題 然後要改product_product_type(OK) & while終止(OK) >> 現在要讓擺不下的設一個error

# Natalia research
# 1. mutation: 一般選品納入

