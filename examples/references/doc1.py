# import libs
from rich import print
from pyThermoDB.references import ReferenceChecker
from mozichem_hub.references import ReferenceMapper
from mozichem_hub.models import Component

# SECTION: reference content
REFERENCE_CONTENT = """
REFERENCES:
    CUSTOM-REF-1:
      DATABOOK-ID: 1
      TABLES:
        ideal-gas-heat-capacity:
          TABLE-ID: 1
          DESCRIPTION:
            This table provides the heat capacity at constant pressure of ideal gas (Cp_IG) in J/mol.K as a function of temperature (T) in K.
          EQUATIONS:
            EQ-1:
              BODY:
                - res['ideal-gas-heat-capacity | Cp_IG | J/mol.K'] = (parms['a0 | a0 | 1'] + parms['a1 | a1 | 1E3']*args['temperature | T | K'] + parms['a2 | a2 | 1E5']*(args['temperature | T | K']**2) + parms['a3 | a3 | 1E8']*(args['temperature | T | K']**3) + parms['a4 | a4 | 1E11']*(args['temperature | T | K']**4))*parms['Universal-Gas-Constant | R | J/mol.K']
              BODY-INTEGRAL:
                  - A1 = parms['a0 | a0 | 1']*args['temperature | T1 | K']
                  - B1 = (parms['a1 | a1 | 1E3']/2)*(args['temperature | T1 | K']**2)
                  - C1 = (parms['a2 | a2 | 1E5']/3)*(args['temperature | T1 | K']**3)
                  - D1 = (parms['a3 | a3 | 1E8']/4)*(args['temperature | T1 | K']**4)
                  - E1 = (parms['a4 | a4 | 1E11']/5)*(args['temperature | T1 | K']**5)
                  - res1 =  A1 + B1 + C1 + D1 + E1
                  - A2 = parms['a0 | a0 | 1']*args['temperature | T2 | K']
                  - B2 = (parms['a1 | a1 | 1E3']/2)*(args['temperature | T2 | K']**2)
                  - C2 = (parms['a2 | a2 | 1E5']/3)*(args['temperature | T2 | K']**3)
                  - D2 = (parms['a3 | a3 | 1E8']/4)*(args['temperature | T2 | K']**4)
                  - E2 = (parms['a4 | a4 | 1E11']/5)*(args['temperature | T2 | K']**5)
                  - res2 =  A2 + B2 + C2 + D2 + E2
                  - res = parms['Universal-Gas-Constant | R | J/mol.K']*(res2 - res1)
              BODY-FIRST-DERIVATIVE:
                  - res = parms['Universal-Gas-Constant | R | J/mol.K']*(parms['a1 | a1 | 1E3'] + 2*parms['a2 | a2 | 1E5']*args['temperature | T | K'] + 3*parms['3 | a3 | 1E8']*(args['temperature | T | K']**2) + 4*parms['a4 | a4 | 1E11']*(args['temperature | T | K']**3))
              BODY-SECOND-DERIVATIVE:
                  - res = parms['Universal-Gas-Constant | R | J/mol.K']*(2*parms['a2 | a2 | 1E5'] + 6*parms['3 | a3 | 1E8']*args['temperature | T | K'] + 12*parms['a4 | a4 | 1E11']*(args['temperature | T | K']**2))
          STRUCTURE:
            COLUMNS: [No.,Name,Formula,State,a0,a1,a2,a3,a4,R,Eq]
            SYMBOL: [None,None,None,None,a0,a1,a2,a3,a4,R,Cp_IG]
            UNIT: [None,None,None,None,1,1E3,1E5,1E8,1E11,1,J/mol.K]
          VALUES:
            - [1,'carbon dioxide','CO2','g',3.259,1.356,1.502,-2.374,1.056,8.314,1]
            - [2,'carbon monoxide','CO','g',3.912,-3.913,1.182,-1.302,0.515,8.314,1]
            - [3,'hydrogen','H2','g',2.883,3.681,-0.772,0.692,-0.213,8.314,1]
            - [4,'methanol','CH3OH','g',4.714,-6.986,4.211,-4.443,1.535,8.314,1]
            - [5,'water','H2O','g',4.395,-4.186,1.405,-1.564,0.632,8.314,1]
            - [6,'acetylene','C2H2','g',2.410,10.926,-0.255,-0.790,0.524,8.314,1]
            - [7,'ethanol','C2H6O','l',4.178,4.427,5.660,6.651,2.487,8.314,1]
            - [8,'n-butane','C4H10','g',5.547,5.536,8.057,-10.571,4.134,8.314,1]
            - [9,'methane','CH4','g',4.568,-8.975,3.631,-3.407,1.091,8.314,1]
            - [10,'propane','C3H8','g',3.847,5.131,6.011,-7.893,3.079,8.314,1]
            - [11,'1-butene','C4H8','g',4.389,7.984,6.143,-8.197,3.165,8.314,1]
            - [12,'1,3-Butadiene','C4H6','g',3.607,5.085,8.253,-12.371,5.321,8.314,1]
            - [13,'ethylene','C2H4','g',4.221,-8.782,5.795,-6.729,2.511,8.314,1]
            - [14,'benzene','C6H6','l',3.551,-6.184,14.365,-19.807,8.234,8.314,1]
            - [15,'nitrogen','N2','g',3.539,-0.261,0.007,0.157,-0.099,8.314,1]
            - [16,'ethane','C2H6','g',4.178,-4.427,5.660,-6.651,2.487,8.314,1]
        general-data:
          TABLE-ID: 2
          DESCRIPTION:
            This table provides the general data of different chemical species participating in the CO2 hydrogenation reaction and includes molecular weight (MW) in g/mol, critical temperature (Tc) in K, critical pressure (Pc) in MPa, and critical molar volume (Vc) in m3/kmol. The table also includes the critical compressibility factor (Zc), acentric factor (AcFa), enthalpy of formation (EnFo) in kJ/mol, and Gibbs energy of formation (GiEnFo) in kJ/mol. The chemical state of the species is also provided in the table and hence the enthalpy of formation and Gibbs energy of formation are provided for the ideal gas and liquid state are designated as EnFo_IG, GiEnFo_IG, EnFo_LIQ, and GiEnFo_LIQ, respectively.
          DATA: []
          STRUCTURE:
            COLUMNS: [No.,Name,Formula,State,Molecular-Weight,Critical-Temperature,Critical-Pressure,Critical-Molar-Volume,Critical-Compressibility-Factor,Acentric-Factor,Enthalpy-of-Formation,Gibbs-Energy-of-Formation]
            SYMBOL: [None,None,None,None,MW,Tc,Pc,Vc,Zc,AcFa,EnFo,GiEnFo]
            UNIT: [None,None,None,None,g/mol,K,MPa,m3/kmol,None,None,kJ/mol,kJ/mol]
            CONVERSION: [None,None,None,None,1,1,1,1,1,1,1,1]
          VALUES:
            - [1,'carbon dioxide','CO2','g',44.01,304.21,7.383,0.094,0.274,0.2236,-393.5,-394.4]
            - [2,'carbon monoxide','CO','g',28.01,132.92,3.499,0.0944,0.299,0.0482,-110.5,-137.2]
            - [3,'hydrogen','H2','g',2.016,33.19,1.313,0.064147,0.305,-0.216,0,0]
            - [4,'methanol','CH3OH','g',32.04,512.5,8.084,0.117,0.222,0.5658,-200.7,-162]
            - [5,'water','H2O','g',18.01,647.096,22.064,0.0559472,0.229,0.3449,-241.8,-228.6]
            - [6,'acetylene','C2H2','g',26.037,308.3,6.138,0.112,0.268,0.1912,227.5,210.0]
            - [7,'ethanol','C2H6O','l',46.068,514,6.137,0.168,0.241,0.6436,-277.70,-174.80]
            - [8,'n-butane','C4H10','g',58.122,425.12,3.796,0.255,0.274,0.2002,-125.80,-16.60]
            - [9,'methane','CH4','g',16.042,190.564,4.599,0.0986,0.286,0.0115,-74.50,-50.50]
            - [10,'propane','C3H8','g',44.096,369.83,4.248,0.2,0.276,0.1523,-104.70,-24.30]
            - [11,'1-butene','C4H8','g',56.106,419.5,4.02,0.241,0.278,0.1845,1.20,70.30]
            - [12,"1,3-Butadiene",'C4H6','g',54.090,425,4.32,0.221,0.27,0.1950,109.20,149.80]
            - [13,'ethylene','C2H4','g',28.053,282.34,5.041,0.131,0.281,0.0862,52.50,68.50]
            - [14,'benzene','C6H6','l',78.112,562.05,4.895,0.256,0.268,0.2103,-49.10,124.5]
            - [15,'nitrogen','N2','g',28.013,126.2,3.4,0.08921,0.289,0.0377,0,0]
            - [16,'ethane','C2H6','g',30.069,305.32,4.872,0.1455,0.279,0.0995,-83.8,-31.9]
        vapor-pressure:
          TABLE-ID: 3
          DESCRIPTION:
            This table provides the vapor pressure (P) in Pa as a function of temperature (T) in K.
          EQUATIONS:
            EQ-1:
              BODY:
                - parms['C1 | C1 | 1'] = parms['C1 | C1 | 1']/1
                - parms['C2 | C2 | 1'] = parms['C2 | C2 | 1']/1
                - parms['C3 | C3 | 1'] = parms['C3 | C3 | 1']/1
                - parms['C4 | C4 | 1'] = parms['C4 | C4 | 1']/1
                - parms['C5 | C5 | 1'] = parms['C5 | C5 | 1']/1
                - res['vapor-pressure | VaPr | Pa'] = math.exp(parms['C1 | C1 | 1'] + parms['C2 | C2 | 1']/args['temperature | T | K'] + parms['C3 | C3 | 1']*math.log(args['temperature | T | K']) + parms['C4 | C4 | 1']*(args['temperature | T | K']**parms['C5 | C5 | 1']))
              BODY-INTEGRAL:
                None
              BODY-FIRST-DERIVATIVE:
                None
              BODY-SECOND-DERIVATIVE:
                None
          STRUCTURE:
            COLUMNS: [No.,Name,Formula,State,C1,C2,C3,C4,C5,Tmin,P(Tmin),Tmax,P(Tmax),Eq]
            SYMBOL: [None,None,None,None,C1,C2,C3,C4,C5,Tmin,P(Tmin),Tmax,P(Tmax),VaPr]
            UNIT: [None,None,None,None,1,1,1,1,1,K,Pa,K,Pa,Pa]
          VALUES:
            - [1,'carbon dioxide','CO2','g',140.54,-4735,-21.268,4.09E-02,1,216.58,5.19E+05,304.21,7.39E+06,1]
            - [2,'carbon monoxide','CO','g',45.698,-1076.6,-4.8814,7.57E-05,2,68.15,1.54E+04,132.92,3.49E+06,1]
            - [3,'hydrogen','H2','g',12.69,-94.9,1.1125,3.29E-04,2,13.95,7.21E+03,33.19,1.32E+06,1]
            - [4,'methanol','CH3OH','g',82.718,-6904.5,-8.8622,7.47E-06,2,175.47,1.11E-01,512.5,8.15E+06,1]
            - [5,'water','H2O','g',73.649,-7258.2,-7.3037,4.17E-06,2,273.16,6.11E+02,647.096,2.19E+07,1]
            - [6,'acetylene','C2H2','g',39.63,-2552.2,-2.78,2.39E-16,6,192.4,1.27E+05,308.3,6.11E+06,1]
            - [7,'ethanol','C2H6O','l',73.304,-7122.3,-7.1424,2.89E-06,2,159.05,4.96E-04,514,6.11E+06,1]
            - [8,'n-butane','C4H10','g',66.343,-4363.2,-7.046,9.45E-06,2,134.86,6.74E-01,425.12,3.77E+06,1]
            - [9,'methane','CH4','g',39.205,-1324.4,-3.4366,3.10E-05,2,90.69,1.17E+04,190.56,4.59E+06,1]
            - [10,'propane','C3H8','g',59.078,-3492.6,-6.0669,1.09E-05,2,85.47,1.68E-04,369.83,4.21E+06,1]
            - [11,'1-butene','C4H8','g',51.836,-4019.2,-4.5229,4.88E-17,6,87.8,6.94E-07,419.5,4.02E+06,1]
            - [12,'1,3-Butadiene','C4H6','g',75.572,-4621.9,-8.5323,1.23E-05,2,164.25,6.92E+01,425,4.30E+06,1]
            - [13,'ethylene','C2H4','g',53.963,-2443,-5.5643,1.91E-05,2,104,1.26E+02,282.34,5.03E+06,1]
            - [14,'benzene','C6H6','l',83.107,-6486.2,-9.2194,6.98E-06,2,278.68,4.76E+03,562.05,4.88E+06,1]
            - [15,'nitrogen','N2','g',58.282,-1084.1,-8.3144,4.41E-02,1,63.15,1.25E+04,126.2,3.39E+06,1]
            - [16,'ethane','C2H6','g',51.857,-2598.7,-5.1283,1.49E-05,2,90.35,1.13E+00,305.32,4.85E+06,1]
        NRTL Non-randomness parameters-1:
          TABLE-ID: 4
          DESCRIPTION:
            This table provides the NRTL non-randomness parameters for the NRTL equation.
          MATRIX-SYMBOL:
            - a
            - b
            - c
            - alpha
          STRUCTURE:
            COLUMNS: [No.,Name,Formula,a_i_1,a_i_2,b_i_1,b_i_2,c_i_1,c_i_2,alpha_i_1,alpha_i_2]
            SYMBOL: [None,None,None,a_i_1,a_i_2,b_i_1,b_i_2,c_i_1,c_i_2,alpha_i_1,alpha_i_2]
            UNIT: [None,None,None,1,1,1,1,1,1,1,1]
          VALUES:
            - [None,None,None,methanol,ethanol,methanol,ethanol,methanol,ethanol,methanol,ethanol]
            - [None,None,None,CH3OH,C2H5OH,CH3OH,C2H5OH,CH3OH,C2H5OH,CH3OH,C2H5OH]
            - [1,methanol,CH3OH,0,0.300492719,0,1.564200272,0,35.05450323,0,4.481683583]
            - [2,ethanol,C2H5OH,0.380229054,0,-20.63243601,0,0.059982839,0,4.481683583,0]
        NRTL Non-randomness parameters-2:
          TABLE-ID: 5
          DESCRIPTION:
            This table provides the NRTL non-randomness parameters for the NRTL equation.
          MATRIX-SYMBOL:
            - a
            - b
            - c
            - alpha
          STRUCTURE:
            COLUMNS: [No.,Mixture,Name,Formula,a_i_1,a_i_2,b_i_1,b_i_2,c_i_1,c_i_2,alpha_i_1,alpha_i_2]
            SYMBOL: [None,None,None,None,a_i_1,a_i_2,b_i_1,b_i_2,c_i_1,c_i_2,alpha_i_1,alpha_i_2]
            UNIT: [None,None,None,None,1,1,1,1,1,1,1,1]
          VALUES:
            - [1,methanol|ethanol,methanol,CH3OH,0,0.300492719,0,1.564200272,0,35.05450323,0,4.481683583]
            - [2,methanol|ethanol,ethanol,C2H5OH,0.380229054,0,-20.63243601,0,0.059982839,0,4.481683583,0]
            - [1,methane|ethanol,methanol,CH3OH,0,0.300492719,0,1.564200272,0,35.05450323,0,4.481683583]
            - [2,methane|ethanol,ethanol,C2H5OH,0.380229054,0,-20.63243601,0,0.059982839,0,4.481683583,0]
"""


# SECTION: create ReferenceChecker instance
ReferenceChecker_ = ReferenceChecker(REFERENCE_CONTENT)

# SECTION: check component availability
component_name = 'carbon dioxide'
component_formula = 'CO2'
component_state = 'g'
# CO2
CO2 = Component(
    name=component_name,
    formula=component_formula,
    state=component_state
)

# check component availability
check_result = ReferenceChecker_.check_component_availability(
    component_name=component_name,
    component_formula=component_formula,
    component_state=component_state,
    databook_name='CUSTOM-REF-1',
)
print(f"Check Result: {check_result}")

# get component reference config
component_reference_config = ReferenceChecker_.get_component_reference_config(
    component_name=component_name,
    component_formula=component_formula,
    component_state=component_state,
    databook_name='CUSTOM-REF-1',
)
print(f"Component Reference Config: {component_reference_config}")

# SECTION: generate reference link (ALL)
reference_config_ = ReferenceChecker_.generate_reference_link(
    databook_name='CUSTOM-REF-1',
)
print(f"Reference Link: {reference_config_}")

# SECTION: generate reference link (specific table)
reference_link_specific = ReferenceChecker_.generate_reference_link(
    databook_name='CUSTOM-REF-1',
    table_names='NRTL Non-randomness parameters-1'
)
print(f"Reference Link (Specific Table): {reference_link_specific}")

# SECTION: generate reference thermodb
ReferenceMapper_ = ReferenceMapper()

reference_thermodb = ReferenceMapper_.\
    _reference_thermodb_generator_from_reference_content(
        reference_content=REFERENCE_CONTENT,
        components=[CO2]
    )
print(f"Reference ThermoDB: {reference_thermodb}")
