# Importerar pytest-biblioteket, som används för att skapa och köra tester

import pytest

# Importerar NetworkConfigManager-klassen som ska testas
from network_config_manager import NetworkConfigManager
 
# Skapar en pytest fixture som hanterar setup och teardown för NetworkConfigManager
# Denna fixture körs före varje test för att skapa och återställa manager-objektet
@pytest.fixture
def setup_method():

    # Skapar en ny instans av NetworkConfigManager
    manager = NetworkConfigManager()

    # Ansluter till manager (exempelvis öppnar en anslutning till en enhet eller nätverksresurs)
    manager.connect()
 
    # Yield gör att pytest kan använda manager-objektet i testen
    yield manager
 
    # Återställer konfigurationerna till deras standardvärden efter att testet är klart
    manager.update_hostname("1")  # Sätter hostname tillbaka till standardvärdet
    manager.update_interface_state("down")  # Sätter interface state tillbaka till "down"
    manager.update_response_prefix("Standard Response")  # Sätter response prefix till standardvärdet

    # Efter att testet har kört och yield har använts, disconnectas manager-objektet
    manager.disconnect()
 
# Testklass som innehåller alla tester för NetworkConfigManager

class TestNetworkConfigManager:
    # Testmetod som verifierar att standardvärdet för hostname är korrekt

    def test_show_hostname_default(self, setup_method):
        # Verifierar att hostname är "1" som är standardvärdet
        assert setup_method.show_hostname() == "hostname: 1"
 
    # Testmetod som verifierar att standardvärdet för interface state är korrekt

    def test_show_interface_state_default(self, setup_method):

        # Verifierar att interface state är "down" som är standardvärdet
        assert setup_method.show_interface_state() == "interface_state: down"
 
    # Testmetod som verifierar att standardvärdet för response prefix är korrekt

    def test_show_response_prefix_default(self, setup_method):
        # Verifierar att response prefix är "Standard Response" som är standardvärdet
        assert setup_method.show_response_prefix() == "response_prefix: Standard Response"
 
    # Testmetod som testar uppdatering av hostname
    def test_update_hostname(self, setup_method):

        # Uppdaterar hostname till "RouterX"
        setup_method.update_hostname("RouterX")

        # Verifierar att hostname nu är "RouterX"
        assert setup_method.show_hostname() == "hostname: RouterX"
 
    # Testmetod som testar uppdatering av interface state

    def test_update_interface_state(self, setup_method): 

        # Uppdaterar interface state till "up"

        setup_method.update_interface_state("up")

        # Verifierar att interface state nu är "up"

        assert setup_method.show_interface_state() == "interface_state: up"

        # Testar om felaktigt värde kastar ett undantag

        with pytest.raises(ValueError):

            # Försöker sätta ett ogiltigt värde på interface state

            setup_method.update_interface_state("invalid_value")
 
    # Testmetod som testar uppdatering av response prefix

    def test_update_response_prefix(self, setup_method):

        # Uppdaterar response prefix till "CustomPrefix:"
        setup_method.update_response_prefix("CustomPrefix:")

        # Verifierar att response prefix nu är "CustomPrefix:"
        assert setup_method.show_response_prefix() == "response_prefix: CustomPrefix:"
 
    # Testmetod som testar uppdatering och verifiering av hostname

    def test_update_and_verify_hostname(self, setup_method):
        new_hostname = "NewRouter"

        # Uppdaterar hostname till "NewRouter"
        setup_method.update_hostname(new_hostname)

        # Verifierar att hostname nu är "NewRouter"
        assert setup_method.show_hostname() == f"hostname: {new_hostname}"
 
    # Testmetod som testar uppdatering och verifiering av interface state

    def test_update_and_verify_interface_state(self, setup_method):
        new_state = "up"

        # Uppdaterar interface state till "up"
        setup_method.update_interface_state(new_state)

        # Verifierar att interface state nu är "up"
        assert setup_method.show_interface_state() == f"interface_state: {new_state}"
 
    # Testmetod som testar uppdatering och verifiering av response prefix

    def test_update_and_verify_response_prefix(self, setup_method):
        new_prefix = "NewResponsePrefix:"

        # Uppdaterar response prefix till "NewResponsePrefix:"

        setup_method.update_response_prefix(new_prefix)

        # Verifierar att response prefix nu är "NewResponsePrefix:"

        assert setup_method.show_response_prefix() == f"response_prefix: {new_prefix}"
 
    # Testmetod som testar att ett fel kastas vid ogiltig interface state

    def test_update_and_verify_interface_state_exception(self, setup_method):
        new_state = "left"  # Ett ogiltigt värde för interface state

        # Förväntar sig ett ValueError undantag när man försöker sätta ett ogiltigt värde

        with pytest.raises(ValueError):
            setup_method.update_interface_state(new_state)
 
# Startar pytest om scriptet körs direkt
if __name__ == "__main__":
    pytest.main()

 