# Arquivo auxiliar para definição de funções
import numpy as np




# Calculo do coeficiente PSI para relaxação do aço
# A partir de um certo nível de tensão:
def calcpsi(tensao):
    psi = np.zeros(tensao.size)
    for i in range(tensao.size):
        if (tensao[i] <= 0.5):
            psi[i] = 0
        elif (tensao[i] <= 0.6):
            extra = tensao[i] - 0.5
            adicional = 13*extra
            psi[i] = (0+adicional)/100
        elif (tensao[i] <= 0.7):
            extra = tensao[i] - 0.6
            adicional = 12*extra
            psi[i] = (1.3+adicional)/100
        else:
            extra = tensao[i] - 0.7
            adicional = 10*extra
            psi[i] = (2.5+adicional)/100
    return psi
    
def calcps(tensao):
    if (tensao <= 0.5):
        return 0
    elif (tensao <= 0.6):
        extra = tensao - 0.5
        adicional = 13*extra
        return (0+adicional)/100
    elif (tensao <= 0.7):
        extra = tensao - 0.6
        adicional = 12*extra
        return (1.3+adicional)/100
    else:
        extra = tensao - 0.7
        adicional = 10*extra
        return (2.5+adicional)/100
    

# Retorna a tensão no aço CP-190 para uma dada deformação
def tensCalc_cp190(x):
    Ep = 20000
    fpyd = round(190*0.9/1.15,2)
    ep_y = fpyd/Ep
    if (x < ep_y):
        return Ep*x
    else:
        return fpyd
    
# Retorna a tensão do aço CA-50 para uma dada deformação
def tensCalc_CA50(x):
    Es = 21000
    fyd = round(50/1.15,2)
    es_y = fyd/Es
    if (x < es_y):
        return Es*x
    else:
        return fyd
    
    
    

# =============================================================================
#   Função para cálculo de seções retangulares de concreto protendido:
#       Bw: largura da seção retangular
#       h: altura da seção retangular
#       fc: alfa_c*f_cd do concreto
#       Ap: área de aço de protensão
#       eps_pn: deformação de neutralização da seção
#       dp: posição da armadura de protensão
#       ds: posição da armadura passiva
#       Md: momento último de cálculo que a seção deve resistir
#
#   UNIDADES: utilizar unidades coerentes
#
# =============================================================================
def linha_neutra_cp_ret(bw, h, fc, Ap, eps_pn, dp, ds, Md):
    x = 0
    continuar = 1
    sigma_s = round(50/1.15 ,2)      # chute inicial para tensão da armadura passiva
    sigma_p = round(190*0.9/1.15,2)  # chute inicial para tensão da armadura ativa
    cont = 0
    while (continuar):
        cont = cont +1
        Rpt = sigma_p*Ap
        a_bh = 1
        b_bh = -2.5*ds
        c_bh = (Md+Rpt*(ds-dp))/(0.32*bw*fc)
        x_1 = (-b_bh + (b_bh**2 - 4*a_bh*c_bh )**0.5)/(2*a_bh)
        x_2 = (-b_bh - (b_bh**2 - 4*a_bh*c_bh )**0.5)/(2*a_bh)
        if (x_1 > h or x_1 < 0):
            x = x_2
        else:
            x = x_1
        
        eps_p = 0.9*eps_pn + 0.0035*(dp-x)/x
        eps_s = 0.0035*(ds-x)/x
        
        sigma_p2 = round(tensCalc_cp190(eps_p),2)
        sigma_s2 = round(tensCalc_CA50(eps_s),2)
        
        if (round(sigma_p,2) == round(sigma_p2,2)):
            if (round(sigma_s,2) == round(sigma_s2,2)):
                continuar = continuar -1
        
        if (cont >= 100):
            continuar = continuar - 1
        
    retorno = [round(x,2),round(eps_p,5),round(eps_s,5),round(Rpt,2),sigma_s,sigma_p]
    return retorno
