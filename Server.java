
import java.net.BindException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;
import java.util.Date;

public class Server {
	private static final Integer PORTA = 6001;
	private static final String IP = "192.168.1.15";

	public static void main(String[] args) {
		System.out.println("O servidor NTP está no ar!");
		DatagramSocket serverSocketUDP = null;
		while (true) {
			try {
					Thread.currentThread().sleep(1000);
					byte[] buffer = new byte[12];
					DatagramPacket pacote = new DatagramPacket(buffer, 12);
					serverSocketUDP.receive(pacote);
					pacote.getAddress();
					String ipServidor = new String(pacote.getData(),StandardCharsets.UTF_8);
					System.out.println("Pacote recebido " + ipServidor);
					if(ipServidor != null && !ipServidor.isEmpty()) {
						
						Date date = new Date();
						date.getTime();
						InetAddress ip = InetAddress.getByName(ipServidor);
						String mensagemEnvio = date.toString();
						byte[] bufferEnvio = mensagemEnvio.getBytes(StandardCharsets.UTF_8);
						System.out.println(bufferEnvio.length);
						DatagramPacket pacoteEnvio = new DatagramPacket(bufferEnvio, bufferEnvio.length, ip, PORTA);
						serverSocketUDP.send(pacoteEnvio);
						System.out.println("Pacote enviado " + mensagemEnvio);
					}
					serverSocketUDP.close();
	
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