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
  print type(of)
  ip_addr = IPAddr(packet.next.dstip) #Cria um objeto do tipo IPAddr para que seja possivel a selecao da faixa de IP;
  ip_conv = ip_addr.toUnsigned() #Converte o IP do formato CIDR para unsigned_int (será usado na análise de subredes)

 
  print '******* EVENTO **********'
  log.info(dpid_to_str(event.dpid))
   
  
  if event.dpid == 1:
    print 'SWITCH 1 OK'
    #ip_addr = ip_addr.split('.')
    print ip_addr.toStr()
    print 'subrede'
    print getSubRede(ip_addr.toStr());
    if  getSubRede(ip_addr.toStr()) == 1:   #Valores para a subrede 10.10.1.0/24
      print 's1 puro'
      porta_out = ip_conv-168427776
      print porta_out
      #msg.idle_timeout = 300                #Tempo de vida do fluxo no tipo idle(soh apaga se n tiver uso)
      msg.match.dl_type=0x800              #dl_type do IPv4
      #msg.match.nw_dstip='10.10.1.'+str(porta_out)
      msg.match.nw_dstip='10.10.1.1'      
      msg.actions.append(of.ofp_action_output(port =1))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
                            #Método p/tratamento dos primeiros paotes (evitar perda)
      event.connection.send(msg) 
      _reenvio(event,1)  

    	
    elif ((ip_conv >= 168428032) and (ip_conv <= 168428287)):
         
      print 's1 para s2'
      #msg.idle_timeout = 300
      msg.match.dl_type=0x800
      msg.match.nw_dst="10.10.2.0/24"
      msg.actions.append(of.ofp_action_output(port=4))
      _reenvio(event, 4)
      event.connection.send(msg)
    
    elif ((ip_conv >= 168428288) and (ip_conv <=168428543)):
        
      print 's1 para s3'
      #msg.idle_timeout = 3000
      msg.match.dl_type=0x800
      msg.match.nw_dst="10.10.3.0/24"
      msg.actions.append(of.ofp_action_output(port=5))             
      _reenvio(event,5)
      event.connection.send(msg)
      
    
  
  elif event.dpid == 2:
    print 'SWITCH 2 OK'
    if  ((ip_conv>= 168428032) and (ip_conv <=168428287)): #Valores para a subrede 10.10.2.0/24
      print 's2 puro'
      porta_out = ip_conv-168428032
      print porta_out
      #msg.idle_timeout = 3000              #Tempo de vida do fluxo no tipo idle(soh apaga se n tiver uso)
      msg.match.dl_type=0x800              #dl_type do IPv4
      msg.match.nw_dstip='10.10.2.1'
      msg.actions.append(of.ofp_action_output(port =1))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,1)                      #Método p/tratamento dos primeiros paotes (evitar perda)
      event.connection.send(msg)
  
    elif ((ip_conv >= 168427777) and (ip_conv <= 168428031)):
      print 's2 para s1'
      #msg.idle_timeout = 3000
      msg.match.dl_type=0x800
      msg.match.nw_dst="10.10.1.0/24"
      msg.actions.append(of.ofp_action_output(port=4))
      _reenvio(event,4)
      event.connection.send(msg)

    elif ((ip_conv >= 168428288) and (ip_conv <=168428543)):
      print 's2 para s3'
      #msg.idle_timeout = 3000
      msg.match.dl_type=0x800
      msg.match.nw_dst="10.10.3.0/24"
      msg.actions.append(of.ofp_action_output(port=5))					
      _reenvio(event,5)
      event.connection.send(msg)
	  
    
##############################################################CONFIG SUBREDE 10.10.3.0/24  
  
  elif event.dpid == 3:
    print 'SWITCH 3 OK'
    if  ((ip_conv >= 168428288) and (ip_conv <=168428543)):      #Valores para subrede 10.10.3.0/24
      print 's3 puro'
      porta_out = ip_conv-168428288
      print porta_out
     # msg.idle_timeout = 3000                #Tempo de vida do fluxo no tipo idle(soh apaga se n tiver uso)
      msg.match.dl_type=0x800              #dl_type do IPv4
      msg.match.nw_dstip='10.10.3.1'
      msg.actions.append(of.ofp_action_output(port =1))  #ENVIA PARA A PORTA DO SWITCH COM O IP DESTINO
      _reenvio(event,1)                      #Método p/tratamento dos primeiros paotes (evitar perda)
      event.connection.send(msg)
	          #INSERIR AÇÃO DE ENVIAR PACOTES "PERDIDOS" (NÃO PERDER PRIMEIROS PACOTES DE CONFIGURAÇÃO)

				        #event.connection.send(msg) #Envia o novo fluxo p/ o switch que solicitou
    elif ((ip_conv >= 168427777) and (ip_conv <= 168428031)):
      print 's3 para s1'
      #msg.idle_timeout = 3000
      msg.match.dl_type=0x800
      msg.match.nw_dst='10.10.1.0/24'
      msg.actions.append(of.ofp_action_output(port=4))
      _reenvio(event,4)
      event.connection.send(msg)

    elif (ip_conv >= 168428032) and (ip_conv <=168428287):
      print 's3 para s2'
      #msg.idle_timeout = 3000
      msg.match.dl_type=0x800
      msg.match.nw_dst='10.10.2.0/24'
      msg.actions.append(of.ofp_action_output(port=5))
      _reenvio(event,5)
      event.connection.send(msg)
    
      
      
  
  
  
def getSubRede(ip_addr):
  return int(ip_addr.split('.')[2])    	

def _reenvio(event, porta):
   print 'porta: '+str(porta)
   #msg2 = of.ofp_packet_out()
   #msg2.data = event.ofp
   #msg2.actions.append(of.ofp_action_output(port = porta)) #provisório
   #event.connection.send(msg2)
    
    
def launch (reactive = True):  #Modo reativo ativado
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn) #Adiciona "escutador de evento" e associa o tratamento com '_handlePacketIn'
    log.info('CONTROLADOR INICIADO')
