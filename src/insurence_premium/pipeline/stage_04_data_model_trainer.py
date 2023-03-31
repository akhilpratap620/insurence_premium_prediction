from insurence_premium.config import ConfigurationManager
from insurence_premium import logger
from insurence_premium.components import ModelTrainer


def main(): 
    logger.info("___________________Data Training has started________________")
    config=ConfigurationManager()
    model_trainer=ModelTrainer(config=config)
    logger.info("training started ")
    model_trainer.get_trained_model()
    logger.info("training completed")


if __name__ =="__main__":
    try:
        main()
    except Exception as e:
        raise e