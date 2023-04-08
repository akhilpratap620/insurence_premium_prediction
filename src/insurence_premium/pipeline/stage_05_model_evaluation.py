from insurence_premium.entity.model_entity import ModelTrainerArtifact
from insurence_premium.config import ConfigurationManager
from insurence_premium.components.data_model_evaluation import ModelEvalution

def main():
    
    con=ConfigurationManager()
    model_evaluation=ModelEvalution(config=con ,model_trainer_artifact=ModelTrainerArtifact)
    model_evaluation.initiate_model_evaluation()


if __name__ =="__main__":
    try:
        main()
    except Exception as e:
        raise e