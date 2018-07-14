
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

		DatagramSocket serverSocketUDP = null;
		while (true) {
			try {
					Thread.currentThread().sleep(1000);
					serverSocketUDP = new DatagramSocket(PORTA);
					Date date = new Date();
					date.getTime();
					InetAddress ip = InetAddress.getByName(IP);
					String mensagem = date.toString();
					byte[] buffer = mensagem.getBytes(StandardCharsets.UTF_8);
					System.out.println(buffer.length);
					DatagramPacket pacote = new DatagramPacket(buffer, buffer.length, ip, PORTA);
					serverSocketUDP.send(pacote);
					System.out.println("Pacote enviado " + mensagem);
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