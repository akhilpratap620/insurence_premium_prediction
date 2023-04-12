from insurence_premium.config import ConfigurationManager
from insurence_premium.components.data_model_pusher import ModelPusher 


def main():

    
    con= ConfigurationManager()
    model_pusher=ModelPusher(config=con)
    model_pusher.export_model()

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        raise e    
