#coding: utf-8

from pox.core import core
import pox.openflow.libopenflow_01 as of 
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
import pox.lib.packet as pkt
from pox.lib.util import dpid_to_str

log = core.getLogger()

def _handle_PacketIn(event):

  packet = event.parsed
  msg = of.ofp_flow_mod()
    ##Mensagens de debug de classes do Python
  
  print '**********************'
  
  ip_entrada = IPAddr(packet.next.dstip)
  ip_addr = ip_entrada.toStr() #Cria um objeto do tipo IPAddr para que seja possivel a selecao da faixa de IP;
  #ip_string = ip_addr.toStr() #Converte o IP do formato CIDR para unsigned_int (será usado na análise de subredes)

 
  print '******* EVENTO **********'
  print 'IP:'+ip_addr+'--subrede:'+str(getSubRede(ip_addr)) 
  print 'subnet: '+str(getSubRede(ip_addr)) 
  print 'porta: '+str(getPorta(ip_addr))  
  
  if event.dpid == 1:
    print 'SWITCH 1 OK'
    
    #print ip_addr.toStr()
    #print 'subrede'
    #print getSubRede(ip_addr.toStr());
    if  getSubRede(ip_addr) == 1:   #Valores para a subrede 10.10.1.0/24
      print 's1 puro'
      msg.idle_timeout = 60                #Tempo de vida do fluxo no tipo idle(soh apaga se n tiver uso)
      msg.match.dl_type=0x800              #dl_type do IPv4
      msg.match.nw_dst ="10.10.1."+str(getPorta(ip_addr))      
      msg.actions.append(of.ofp_action_output(port = getPorta(ip_addr)))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,getPorta(ip_addr))                      #Método p/tratamento dos primeiros paotes (evitar perda)
      event.connection.send(msg) 
        

    	
    elif getSubRede(ip_addr) == 2:
      print 's1 para s2'
      msg.idle_timeout = 60
      msg.match.dl_type=0x800
      msg.match.nw_dst= "10.10.2."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 4))
      _reenvio(event, 4)
      event.connection.send(msg)
    
    elif getSubRede(ip_addr) == 3:
        
      print 's1 para s3'
      msg.idle_timeout = 60
      msg.match.dl_type=0x800
      msg.match.nw_dst= "10.10.3."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 5))             
      _reenvio(event,5)
      event.connection.send(msg)
      
    
  
  elif event.dpid == 2:
    print 'SWITCH 2 OK'
    if getSubRede(ip_addr) == 2: #Valores para a subrede 10.10.2.0/24
      print 's2 puro'
      msg.idle_timeout = 60              #Tempo de vida do fluxo no tipo idle(soh apaga se n tiver uso)
      msg.match.dl_type=0x800              #dl_type do IPv4
      msg.match.nw_dst= "10.10.2."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = getPorta(ip_addr)))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,getPorta(ip_addr))                      #Método p/tratamento dos primeiros paotes (evitar perda)
      event.connection.send(msg)
  
    elif getSubRede(ip_addr) == 1:
      print 's2 para s1'
      msg.idle_timeout = 60
      msg.match.dl_type=0x800
      msg.match.nw_dst= "10.10.1."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 4))
      _reenvio(event,4)
      event.connection.send(msg)

    elif getSubRede(ip_addr) == 3:
      print 's2 para s3'
      msg.idle_timeout = 60
      msg.match.dl_type=0x800
      msg.match.nw_dst= "10.10.3."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 5))					
      _reenvio(event,5)
      event.connection.send(msg)
	  
    
##############################################################CONFIG SUBREDE 10.10.3.0/24  
  
  elif event.dpid == 3:
    print 'SWITCH 3 OK'
    if getSubRede(ip_addr) == 3:      #Valores para subrede 10.10.3.0/24
      print 's3 puro'
      msg.idle_timeout = 60                #Tempo de vida do fluxo no tipo idle(soh apaga se n tiver uso)
      msg.match.dl_type=0x800              #dl_type do IPv4
      msg.match.nw_dst= "10.10.3."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = getPorta(ip_addr)))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,getPorta(ip_addr))                      #Método p/tratamento dos primeiros paotes (evitar perda)
      event.connection.send(msg)
	          #INSERIR AÇÃO DE ENVIAR PACOTES "PERDIDOS" (NÃO PERDER PRIMEIROS PACOTES DE CONFIGURAÇÃO)

				        #event.connection.send(msg) #Envia o novo fluxo p/ o switch que solicitou
    elif getSubRede(ip_addr) == 1:
      print 's3 para s1'
      msg.idle_timeout = 60
      msg.match.dl_type=0x800
      msg.match.nw_dst= "10.10.1."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 4))
      _reenvio(event,4)
      event.connection.send(msg)

    elif getSubRede(ip_addr) == 2:
      print 's3 para s2'
      msg.idle_timeout = 60
      msg.match.dl_type=0x800
      msg.match.nw_dst= "10.10.2."+str(getPorta(ip_addr))
      msg.actions.append(of.ofp_action_output(port = 5))
      _reenvio(event,5)
      event.connection.send(msg)
    
      
      
  
def getPorta(ip_addr):
  return int(ip_addr.split('.')[3])  #pega a porta de determinado host-destino baseado no seu ip --> 10.10.1.2 = porta 2  
  
def getSubRede(ip_addr):
  return int(ip_addr.split('.')[2])    	

def _reenvio(event, porta):
   #print 'porta: '+str(porta)
   msg2 = of.ofp_packet_out()
   msg2.data = event.ofp
   msg2.actions.append(of.ofp_action_output(port = porta)) #provisório
   event.connection.send(msg2)
    
    
def launch (reactive = True):  #Modo reativo ativado
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn) #Adiciona "escutador de evento" e associa o tratamento com '_handlePacketIn'
    log.info('CONTROLADOR INICIADO')
