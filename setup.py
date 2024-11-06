from setuptools import setup, find_packages

setup(
    name="flutter_application_ai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # الحزم الأساسية المطلوبة للعمل
        "numpy",  # مثال على حزمة أساسية
        "scikit-learn",  # مثال آخر
    ],
    extras_require={
        'dev': [
            "pywin32",  # مكتبة pywin32 ستتم إضافتها فقط في بيئة التطوير
        ]
    },
)

