# import libs
from mozichem_hub.references import ReferenceMapper
from mozichem_hub.models import References
# log
from rich import print


# SECTION: custom reference settings
# NOTE: default reference for the ThermoDB
REFERENCE_CONTENT = """
# REFERENCES

## CUSTOM-REF-2

DATABOOK-ID: 1

### vapor-pressure

TABLE-ID: 1

DESCRIPTION: This table provides the vapor pressure (P) in Pa as a function of temperature (T) in K.

EQUATIONS:

- EQ-1:
  - BODY:
    - parms['C1 | C1 | 1'] = parms['C1 | C1 | 1']/1
    - parms['C2 | C2 | 1'] = parms['C2 | C2 | 1']/1
    - parms['C3 | C3 | 1'] = parms['C3 | C3 | 1']/1
    - parms['C4 | C4 | 1'] = parms['C4 | C4 | 1']/1
    - parms['C5 | C5 | 1'] = parms['C5 | C5 | 1']/1
    - res['vapor-pressure | VaPr | Pa'] = math.exp(parms['C1 | C1 | 1'] + parms['C2 | C2 | 1']/args['temperature | T | K'] + parms['C3 | C3 | 1']*math.log(args['temperature | T | K']) + parms['C4 | C4 | 1']*(args['temperature | T | K']**parms['C5 | C5 | 1']))
  - BODY-INTEGRAL:
  - BODY-FIRST-DERIVATIVE:
  - BODY-SECOND-DERIVATIVE:

STRUCTURE:

- COLUMNS: [No.,Name,Formula,State,C1,C2,C3,C4,C5,Tmin,P(Tmin),Tmax,P(Tmax),Eq]
- SYMBOL: [None,None,None,None,C1,C2,C3,C4,C5,Tmin,P(Tmin),Tmax,P(Tmax),VaPr]
- UNIT: [None,None,None,None,1,1,1,1,1,K,Pa,K,Pa,Pa]

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
- [17,'toluene','C7H8','l',76.945,-6729.8,-8.179,5.30E-06,2,178.18,4.75E-02,591.75,4.08E+06,1]

### general-data

TABLE-ID: 2

DESCRIPTION: This table provides the general data of different chemical species participating in the CO2 hydrogenation reaction and includes molecular weight (MW) in g/mol, critical temperature (Tc) in K, critical pressure (Pc) in MPa, and critical molar volume (Vc) in m3/kmol. The table also includes the critical compressibility factor (Zc), acentric factor (AcFa), enthalpy of formation (EnFo) in kJ/mol, and Gibbs energy of formation (GiEnFo) in kJ/mol. The chemical state of the species is also provided in the table and hence the enthalpy of formation and Gibbs energy of formation are provided for the ideal gas and liquid state are designated as EnFo_IG, GiEnFo_IG, EnFo_LIQ, and GiEnFo_LIQ, respectively.

DATA: []

STRUCTURE:

- COLUMNS: [No.,Name,Formula,State,Molecular-Weight,Critical-Temperature,Critical-Pressure,Critical-Molar-Volume,Critical-Compressibility-Factor,Acentric-Factor,Enthalpy-of-Formation,Gibbs-Energy-of-Formation]
- SYMBOL: [None,None,None,None,MW,Tc,Pc,Vc,Zc,AcFa,EnFo,GiEnFo]
- UNIT: [None,None,None,None,g/mol,K,MPa,m3/kmol,None,None,kJ/mol,kJ/mol]
- CONVERSION: [None,None,None,None,1,1,1,1,1,1,1,1]

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
- [17,'toluene','C7H8','l',92.138,591.75,4.108,0.316,0.264,0.2640,12.2,113.6]

EXTERNAL-REFERENCES:

- url1
- url2
"""

# NOTE reference config
REFERENCE_CONFIG = """
# Configs

## ALL

vapor-pressure:

- databook: CUSTOM-REF-2
- table: vapor-pressure
- mode: EQUATIONS
- label: VaPr

general:

- databook: CUSTOM-REF-2
- table: general-data
- mode: DATA
- labels:
  - critical-pressure: Pc
  - critical-temperature: Tc
  - acentric-factor: AcFa
"""

REFERENCE_CONFIG_YAML = """
ALL:
  vapor-pressure:
    databook: CUSTOM-REF-2
    table: vapor-pressure
    mode: EQUATIONS
    label: VaPr
  general:
    databook: CUSTOM-REF-2
    table: general-data
    mode: DATA
    labels:
      critical-pressure: Pc
      critical-temperature: Tc
      acentric-factor: AcFa
"""

# SECTION: custom reference
result = ReferenceMapper()

# NOTE: generate reference
references: References = result._reference_input_settings(
    reference_content=REFERENCE_CONTENT,
    reference_config=REFERENCE_CONFIG_YAML
)
print(f"References: {references}")

# NOTE: convert to reference thermodb
reference_thermodb = result._reference_thermodb_generator(
    references=references,
)
print(f"Reference ThermoDB: {reference_thermodb}")
