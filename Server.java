import java.net.BindException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;
import java.util.Date;

public class Server {
	private static final Integer PORTA = 6001;

	public static void main(String[] args) throws SocketException {

		DatagramSocket serverSocketUDP =  new DatagramSocket(PORTA);
		System.out.println("Sincronizador funcionando");
		while (true) {
			try {
				
				Thread.currentThread().sleep(1000);
				byte[] bufferConsulta = new byte[5];
				DatagramPacket pacote = new DatagramPacket(bufferConsulta,5);
				serverSocketUDP.receive(pacote);
				if(pacote.getData() != null && pacote.getData().length > 0) {
					String mensagemRecebida = new String(pacote.getData(),StandardCharsets.UTF_8);
					System.out.println("Pacote recebido " + mensagemRecebida);
				        InetAddress ip = pacote.getAddress();
				
					if(ip != null ) {
					
						Date date = new Date();
						date.getTime();
						String mensagemEnviada = date.toString();
						byte[] buffer = mensagemEnviada.getBytes(StandardCharsets.UTF_8);
						System.out.println(buffer.length);
						DatagramPacket pacoteEnvio = new DatagramPacket(buffer, buffer.length, ip, PORTA);
						serverSocketUDP.send(pacoteEnvio);
						System.out.println("Pacote enviado " + mensagemEnviada);
						//serverSocketUDP.close();
					}
				}
//				serverSocketUDP.close();
			} catch(BindException be) {
				System.out.println(be.getMessage());
			}catch (Exception e) {
				if (serverSocketUDP != null) {
					serverSocketUDP.close();
				}
				e.printStackTrace();
			}

		}
	}
	
}
