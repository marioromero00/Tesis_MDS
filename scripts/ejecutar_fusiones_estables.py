"""Nueva ejecucion completa con prediccion serial y procedencia registrada."""
import explorar_fusiones as experiment
from threadpoolctl import threadpool_limits

original_factory=experiment.make_model
original_write=experiment.write_json


def serial_model(name,seed):
    model=original_factory(name,seed)
    if hasattr(model.named_steps['model'],'n_jobs'):
        model.named_steps['model'].set_params(n_jobs=1)
    return model


def provenance(path,value):
    if path.name=='protocolo.json':
        value['sources']['ejecutar_fusiones_estables.py']=experiment.digest(__file__)
        value['execution_wrapper']='serial Extra Trees fitting/prediction for deterministic probability reduction'
    original_write(path,value)


if __name__=='__main__':
    experiment.make_model=serial_model
    experiment.write_json=provenance
    with threadpool_limits(limits=4): experiment.main()
