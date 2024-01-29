import unittest
import labsonar_synthesis.scenario.scenario_controller as scenarioController
import labsonar_synthesis.scenario.hydrophone as hydro
import labsonar_synthesis.scenario.ship as ships



class TestScenarioController(unittest.TestCase):

    def setUp(self):
        # Inicialização básica para os testes
        self.scenario = scenarioController.ScenarioController(dimension=3)
        self.ship = ships.Ship(position=(0, 0, 0))
        self.hydrophone = hydro.Hydrophone(position=(100, 100, -10))

    def test_add_object(self):
        # Teste para adicionar objetos ao cenário
        self.scenario.add_object(self.ship)
        self.scenario.add_object(self.hydrophone)
        self.assertIn(self.ship, self.scenario._objects)
        self.assertIn(self.hydrophone, self.scenario._objects)

    def test_simulate_movement(self):
        # Teste para simular movimento
        self.scenario.add_object(self.ship)
        self.scenario.add_object(self.hydrophone)

        ship_movements = {self.ship: ([200, 200, -20], 10)}
        hydrophone_movements = {self.hydrophone: ([150, 150, -15], 5)}

        self.scenario.simulate_movement(ship_movements, hydrophone_movements)
        # Verifica se os objetos se moveram
        self.assertEqual(self.ship.position, [200, 200, -20])
        self.assertEqual(self.hydrophone.position, [150, 150, -15])

    def test_plot_components(self):
        # Teste para verificar a geração de plotagens
        self.scenario.add_object(self.ship)
        self.scenario.add_object(self.hydrophone)
        
        # Aqui, você pode testar se os arquivos de plotagem são gerados corretamente
        # Isso pode envolver verificar se os arquivos são criados no sistema de arquivos

if __name__ == '__main__':
    unittest.main()
