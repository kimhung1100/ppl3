# Generated from main/mt22/parser/MT22.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from lexererr import *



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2=")
        buf.write("\u01eb\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\3\2\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3")
        buf.write("\6\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\b\3\t")
        buf.write("\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13")
        buf.write("\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r")
        buf.write("\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3\16\3")
        buf.write("\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\20")
        buf.write("\3\21\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\23\3\23")
        buf.write("\3\23\3\23\3\23\3\23\3\23\3\23\3\23\3\24\3\24\3\24\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26")
        buf.write("\3\26\3\26\3\27\3\27\3\30\3\30\3\31\3\31\3\32\3\32\3\33")
        buf.write("\3\33\3\34\3\34\3\35\3\35\3\35\3\36\3\36\3\36\3\37\3\37")
        buf.write("\3\37\3 \3 \3 \3!\3!\3\"\3\"\3\"\3#\3#\3$\3$\3$\3%\3%")
        buf.write("\3%\3&\3&\3\'\3\'\3(\3(\3)\3)\3*\3*\3+\3+\3,\3,\3-\3-")
        buf.write("\3.\3.\3/\3/\3\60\3\60\3\61\3\61\7\61\u0140\n\61\f\61")
        buf.write("\16\61\u0143\13\61\3\62\3\62\3\62\7\62\u0148\n\62\f\62")
        buf.write("\16\62\u014b\13\62\3\62\5\62\u014e\n\62\3\62\6\62\u0151")
        buf.write("\n\62\r\62\16\62\u0152\7\62\u0155\n\62\f\62\16\62\u0158")
        buf.write("\13\62\3\62\5\62\u015b\n\62\3\63\3\63\3\63\7\63\u0160")
        buf.write("\n\63\f\63\16\63\u0163\13\63\3\63\5\63\u0166\n\63\3\63")
        buf.write("\6\63\u0169\n\63\r\63\16\63\u016a\7\63\u016d\n\63\f\63")
        buf.write("\16\63\u0170\13\63\3\63\5\63\u0173\n\63\3\64\3\64\3\64")
        buf.write("\3\64\3\64\5\64\u017a\n\64\3\64\3\64\3\64\3\64\3\64\5")
        buf.write("\64\u0181\n\64\3\64\3\64\3\65\3\65\3\66\3\66\7\66\u0189")
        buf.write("\n\66\f\66\16\66\u018c\13\66\3\67\3\67\5\67\u0190\n\67")
        buf.write("\3\67\6\67\u0193\n\67\r\67\16\67\u0194\38\38\39\39\59")
        buf.write("\u019b\n9\3:\3:\7:\u019f\n:\f:\16:\u01a2\13:\3:\3:\3:")
        buf.write("\3;\3;\3;\3;\5;\u01ab\n;\3<\3<\3<\3=\3=\3=\3>\3>\7>\u01b5")
        buf.write("\n>\f>\16>\u01b8\13>\3>\5>\u01bb\n>\3>\3>\3?\3?\7?\u01c1")
        buf.write("\n?\f?\16?\u01c4\13?\3?\3?\3?\3@\3@\3@\3@\7@\u01cd\n@")
        buf.write("\f@\16@\u01d0\13@\3@\3@\3A\3A\3A\3A\7A\u01d8\nA\fA\16")
        buf.write("A\u01db\13A\3A\3A\3A\3A\3A\3B\6B\u01e3\nB\rB\16B\u01e4")
        buf.write("\3B\3B\3C\3C\3C\3\u01d9\2D\3\3\5\4\7\5\t\6\13\7\r\b\17")
        buf.write("\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23")
        buf.write("%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67\359\36")
        buf.write(";\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61a\62c\63")
        buf.write("e\64g\65i\2k\2m\2o\2q\66s\67u\2w\2y\2{8}9\177:\u0081;")
        buf.write("\u0083<\u0085=\3\2\r\5\2C\\aac|\6\2\62;C\\aac|\3\2\63")
        buf.write(";\3\2\62;\4\2GGgg\4\2--//\6\2\n\f\16\17$$^^\n\2$$))^^")
        buf.write("ddhhppttvv\5\3\n\f\16\17^^\4\2\f\f\17\17\5\2\n\f\16\17")
        buf.write("\"\"\2\u01fd\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3")
        buf.write("\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2")
        buf.write("\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2")
        buf.write("\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2")
        buf.write("#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2")
        buf.write("\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65")
        buf.write("\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2")
        buf.write("\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2")
        buf.write("\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2Q\3\2")
        buf.write("\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2\2[\3")
        buf.write("\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e")
        buf.write("\3\2\2\2\2g\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2{\3\2\2\2\2")
        buf.write("}\3\2\2\2\2\177\3\2\2\2\2\u0081\3\2\2\2\2\u0083\3\2\2")
        buf.write("\2\2\u0085\3\2\2\2\3\u0087\3\2\2\2\5\u008c\3\2\2\2\7\u0092")
        buf.write("\3\2\2\2\t\u009a\3\2\2\2\13\u009d\3\2\2\2\r\u00a2\3\2")
        buf.write("\2\2\17\u00a8\3\2\2\2\21\u00ae\3\2\2\2\23\u00b2\3\2\2")
        buf.write("\2\25\u00bb\3\2\2\2\27\u00be\3\2\2\2\31\u00c6\3\2\2\2")
        buf.write("\33\u00cd\3\2\2\2\35\u00d4\3\2\2\2\37\u00d9\3\2\2\2!\u00df")
        buf.write("\3\2\2\2#\u00e4\3\2\2\2%\u00e8\3\2\2\2\'\u00f1\3\2\2\2")
        buf.write(")\u00f4\3\2\2\2+\u00fc\3\2\2\2-\u0102\3\2\2\2/\u0104\3")
        buf.write("\2\2\2\61\u0106\3\2\2\2\63\u0108\3\2\2\2\65\u010a\3\2")
        buf.write("\2\2\67\u010c\3\2\2\29\u010e\3\2\2\2;\u0111\3\2\2\2=\u0114")
        buf.write("\3\2\2\2?\u0117\3\2\2\2A\u011a\3\2\2\2C\u011c\3\2\2\2")
        buf.write("E\u011f\3\2\2\2G\u0121\3\2\2\2I\u0124\3\2\2\2K\u0127\3")
        buf.write("\2\2\2M\u0129\3\2\2\2O\u012b\3\2\2\2Q\u012d\3\2\2\2S\u012f")
        buf.write("\3\2\2\2U\u0131\3\2\2\2W\u0133\3\2\2\2Y\u0135\3\2\2\2")
        buf.write("[\u0137\3\2\2\2]\u0139\3\2\2\2_\u013b\3\2\2\2a\u013d\3")
        buf.write("\2\2\2c\u015a\3\2\2\2e\u0172\3\2\2\2g\u0180\3\2\2\2i\u0184")
        buf.write("\3\2\2\2k\u0186\3\2\2\2m\u018d\3\2\2\2o\u0196\3\2\2\2")
        buf.write("q\u019a\3\2\2\2s\u019c\3\2\2\2u\u01aa\3\2\2\2w\u01ac\3")
        buf.write("\2\2\2y\u01af\3\2\2\2{\u01b2\3\2\2\2}\u01be\3\2\2\2\177")
        buf.write("\u01c8\3\2\2\2\u0081\u01d3\3\2\2\2\u0083\u01e2\3\2\2\2")
        buf.write("\u0085\u01e8\3\2\2\2\u0087\u0088\7c\2\2\u0088\u0089\7")
        buf.write("w\2\2\u0089\u008a\7v\2\2\u008a\u008b\7q\2\2\u008b\4\3")
        buf.write("\2\2\2\u008c\u008d\7d\2\2\u008d\u008e\7t\2\2\u008e\u008f")
        buf.write("\7g\2\2\u008f\u0090\7c\2\2\u0090\u0091\7m\2\2\u0091\6")
        buf.write("\3\2\2\2\u0092\u0093\7d\2\2\u0093\u0094\7q\2\2\u0094\u0095")
        buf.write("\7q\2\2\u0095\u0096\7n\2\2\u0096\u0097\7g\2\2\u0097\u0098")
        buf.write("\7c\2\2\u0098\u0099\7p\2\2\u0099\b\3\2\2\2\u009a\u009b")
        buf.write("\7f\2\2\u009b\u009c\7q\2\2\u009c\n\3\2\2\2\u009d\u009e")
        buf.write("\7g\2\2\u009e\u009f\7n\2\2\u009f\u00a0\7u\2\2\u00a0\u00a1")
        buf.write("\7g\2\2\u00a1\f\3\2\2\2\u00a2\u00a3\7h\2\2\u00a3\u00a4")
        buf.write("\7c\2\2\u00a4\u00a5\7n\2\2\u00a5\u00a6\7u\2\2\u00a6\u00a7")
        buf.write("\7g\2\2\u00a7\16\3\2\2\2\u00a8\u00a9\7h\2\2\u00a9\u00aa")
        buf.write("\7n\2\2\u00aa\u00ab\7q\2\2\u00ab\u00ac\7c\2\2\u00ac\u00ad")
        buf.write("\7v\2\2\u00ad\20\3\2\2\2\u00ae\u00af\7h\2\2\u00af\u00b0")
        buf.write("\7q\2\2\u00b0\u00b1\7t\2\2\u00b1\22\3\2\2\2\u00b2\u00b3")
        buf.write("\7h\2\2\u00b3\u00b4\7w\2\2\u00b4\u00b5\7p\2\2\u00b5\u00b6")
        buf.write("\7e\2\2\u00b6\u00b7\7v\2\2\u00b7\u00b8\7k\2\2\u00b8\u00b9")
        buf.write("\7q\2\2\u00b9\u00ba\7p\2\2\u00ba\24\3\2\2\2\u00bb\u00bc")
        buf.write("\7k\2\2\u00bc\u00bd\7h\2\2\u00bd\26\3\2\2\2\u00be\u00bf")
        buf.write("\7k\2\2\u00bf\u00c0\7p\2\2\u00c0\u00c1\7v\2\2\u00c1\u00c2")
        buf.write("\7g\2\2\u00c2\u00c3\7i\2\2\u00c3\u00c4\7g\2\2\u00c4\u00c5")
        buf.write("\7t\2\2\u00c5\30\3\2\2\2\u00c6\u00c7\7t\2\2\u00c7\u00c8")
        buf.write("\7g\2\2\u00c8\u00c9\7v\2\2\u00c9\u00ca\7w\2\2\u00ca\u00cb")
        buf.write("\7t\2\2\u00cb\u00cc\7p\2\2\u00cc\32\3\2\2\2\u00cd\u00ce")
        buf.write("\7u\2\2\u00ce\u00cf\7v\2\2\u00cf\u00d0\7t\2\2\u00d0\u00d1")
        buf.write("\7k\2\2\u00d1\u00d2\7p\2\2\u00d2\u00d3\7i\2\2\u00d3\34")
        buf.write("\3\2\2\2\u00d4\u00d5\7v\2\2\u00d5\u00d6\7t\2\2\u00d6\u00d7")
        buf.write("\7w\2\2\u00d7\u00d8\7g\2\2\u00d8\36\3\2\2\2\u00d9\u00da")
        buf.write("\7y\2\2\u00da\u00db\7j\2\2\u00db\u00dc\7k\2\2\u00dc\u00dd")
        buf.write("\7n\2\2\u00dd\u00de\7g\2\2\u00de \3\2\2\2\u00df\u00e0")
        buf.write("\7x\2\2\u00e0\u00e1\7q\2\2\u00e1\u00e2\7k\2\2\u00e2\u00e3")
        buf.write("\7f\2\2\u00e3\"\3\2\2\2\u00e4\u00e5\7q\2\2\u00e5\u00e6")
        buf.write("\7w\2\2\u00e6\u00e7\7v\2\2\u00e7$\3\2\2\2\u00e8\u00e9")
        buf.write("\7e\2\2\u00e9\u00ea\7q\2\2\u00ea\u00eb\7p\2\2\u00eb\u00ec")
        buf.write("\7v\2\2\u00ec\u00ed\7k\2\2\u00ed\u00ee\7p\2\2\u00ee\u00ef")
        buf.write("\7w\2\2\u00ef\u00f0\7g\2\2\u00f0&\3\2\2\2\u00f1\u00f2")
        buf.write("\7q\2\2\u00f2\u00f3\7h\2\2\u00f3(\3\2\2\2\u00f4\u00f5")
        buf.write("\7k\2\2\u00f5\u00f6\7p\2\2\u00f6\u00f7\7j\2\2\u00f7\u00f8")
        buf.write("\7g\2\2\u00f8\u00f9\7t\2\2\u00f9\u00fa\7k\2\2\u00fa\u00fb")
        buf.write("\7v\2\2\u00fb*\3\2\2\2\u00fc\u00fd\7c\2\2\u00fd\u00fe")
        buf.write("\7t\2\2\u00fe\u00ff\7t\2\2\u00ff\u0100\7c\2\2\u0100\u0101")
        buf.write("\7{\2\2\u0101,\3\2\2\2\u0102\u0103\7-\2\2\u0103.\3\2\2")
        buf.write("\2\u0104\u0105\7/\2\2\u0105\60\3\2\2\2\u0106\u0107\7,")
        buf.write("\2\2\u0107\62\3\2\2\2\u0108\u0109\7\61\2\2\u0109\64\3")
        buf.write("\2\2\2\u010a\u010b\7\'\2\2\u010b\66\3\2\2\2\u010c\u010d")
        buf.write("\7#\2\2\u010d8\3\2\2\2\u010e\u010f\7(\2\2\u010f\u0110")
        buf.write("\7(\2\2\u0110:\3\2\2\2\u0111\u0112\7~\2\2\u0112\u0113")
        buf.write("\7~\2\2\u0113<\3\2\2\2\u0114\u0115\7?\2\2\u0115\u0116")
        buf.write("\7?\2\2\u0116>\3\2\2\2\u0117\u0118\7#\2\2\u0118\u0119")
        buf.write("\7?\2\2\u0119@\3\2\2\2\u011a\u011b\7>\2\2\u011bB\3\2\2")
        buf.write("\2\u011c\u011d\7>\2\2\u011d\u011e\7?\2\2\u011eD\3\2\2")
        buf.write("\2\u011f\u0120\7@\2\2\u0120F\3\2\2\2\u0121\u0122\7@\2")
        buf.write("\2\u0122\u0123\7?\2\2\u0123H\3\2\2\2\u0124\u0125\7<\2")
        buf.write("\2\u0125\u0126\7<\2\2\u0126J\3\2\2\2\u0127\u0128\7*\2")
        buf.write("\2\u0128L\3\2\2\2\u0129\u012a\7+\2\2\u012aN\3\2\2\2\u012b")
        buf.write("\u012c\7]\2\2\u012cP\3\2\2\2\u012d\u012e\7_\2\2\u012e")
        buf.write("R\3\2\2\2\u012f\u0130\7\60\2\2\u0130T\3\2\2\2\u0131\u0132")
        buf.write("\7.\2\2\u0132V\3\2\2\2\u0133\u0134\7=\2\2\u0134X\3\2\2")
        buf.write("\2\u0135\u0136\7<\2\2\u0136Z\3\2\2\2\u0137\u0138\7}\2")
        buf.write("\2\u0138\\\3\2\2\2\u0139\u013a\7\177\2\2\u013a^\3\2\2")
        buf.write("\2\u013b\u013c\7?\2\2\u013c`\3\2\2\2\u013d\u0141\t\2\2")
        buf.write("\2\u013e\u0140\t\3\2\2\u013f\u013e\3\2\2\2\u0140\u0143")
        buf.write("\3\2\2\2\u0141\u013f\3\2\2\2\u0141\u0142\3\2\2\2\u0142")
        buf.write("b\3\2\2\2\u0143\u0141\3\2\2\2\u0144\u015b\4\62;\2\u0145")
        buf.write("\u0149\t\4\2\2\u0146\u0148\t\5\2\2\u0147\u0146\3\2\2\2")
        buf.write("\u0148\u014b\3\2\2\2\u0149\u0147\3\2\2\2\u0149\u014a\3")
        buf.write("\2\2\2\u014a\u0156\3\2\2\2\u014b\u0149\3\2\2\2\u014c\u014e")
        buf.write("\7a\2\2\u014d\u014c\3\2\2\2\u014d\u014e\3\2\2\2\u014e")
        buf.write("\u0150\3\2\2\2\u014f\u0151\t\5\2\2\u0150\u014f\3\2\2\2")
        buf.write("\u0151\u0152\3\2\2\2\u0152\u0150\3\2\2\2\u0152\u0153\3")
        buf.write("\2\2\2\u0153\u0155\3\2\2\2\u0154\u014d\3\2\2\2\u0155\u0158")
        buf.write("\3\2\2\2\u0156\u0154\3\2\2\2\u0156\u0157\3\2\2\2\u0157")
        buf.write("\u0159\3\2\2\2\u0158\u0156\3\2\2\2\u0159\u015b\b\62\2")
        buf.write("\2\u015a\u0144\3\2\2\2\u015a\u0145\3\2\2\2\u015bd\3\2")
        buf.write("\2\2\u015c\u0173\t\5\2\2\u015d\u0161\t\4\2\2\u015e\u0160")
        buf.write("\t\5\2\2\u015f\u015e\3\2\2\2\u0160\u0163\3\2\2\2\u0161")
        buf.write("\u015f\3\2\2\2\u0161\u0162\3\2\2\2\u0162\u016e\3\2\2\2")
        buf.write("\u0163\u0161\3\2\2\2\u0164\u0166\7a\2\2\u0165\u0164\3")
        buf.write("\2\2\2\u0165\u0166\3\2\2\2\u0166\u0168\3\2\2\2\u0167\u0169")
        buf.write("\t\5\2\2\u0168\u0167\3\2\2\2\u0169\u016a\3\2\2\2\u016a")
        buf.write("\u0168\3\2\2\2\u016a\u016b\3\2\2\2\u016b\u016d\3\2\2\2")
        buf.write("\u016c\u0165\3\2\2\2\u016d\u0170\3\2\2\2\u016e\u016c\3")
        buf.write("\2\2\2\u016e\u016f\3\2\2\2\u016f\u0171\3\2\2\2\u0170\u016e")
        buf.write("\3\2\2\2\u0171\u0173\b\63\3\2\u0172\u015c\3\2\2\2\u0172")
        buf.write("\u015d\3\2\2\2\u0173f\3\2\2\2\u0174\u0175\5i\65\2\u0175")
        buf.write("\u0176\5k\66\2\u0176\u0181\3\2\2\2\u0177\u0179\5i\65\2")
        buf.write("\u0178\u017a\5k\66\2\u0179\u0178\3\2\2\2\u0179\u017a\3")
        buf.write("\2\2\2\u017a\u017b\3\2\2\2\u017b\u017c\5m\67\2\u017c\u0181")
        buf.write("\3\2\2\2\u017d\u017e\5k\66\2\u017e\u017f\5m\67\2\u017f")
        buf.write("\u0181\3\2\2\2\u0180\u0174\3\2\2\2\u0180\u0177\3\2\2\2")
        buf.write("\u0180\u017d\3\2\2\2\u0181\u0182\3\2\2\2\u0182\u0183\b")
        buf.write("\64\4\2\u0183h\3\2\2\2\u0184\u0185\5c\62\2\u0185j\3\2")
        buf.write("\2\2\u0186\u018a\5S*\2\u0187\u0189\5o8\2\u0188\u0187\3")
        buf.write("\2\2\2\u0189\u018c\3\2\2\2\u018a\u0188\3\2\2\2\u018a\u018b")
        buf.write("\3\2\2\2\u018bl\3\2\2\2\u018c\u018a\3\2\2\2\u018d\u018f")
        buf.write("\t\6\2\2\u018e\u0190\t\7\2\2\u018f\u018e\3\2\2\2\u018f")
        buf.write("\u0190\3\2\2\2\u0190\u0192\3\2\2\2\u0191\u0193\5o8\2\u0192")
        buf.write("\u0191\3\2\2\2\u0193\u0194\3\2\2\2\u0194\u0192\3\2\2\2")
        buf.write("\u0194\u0195\3\2\2\2\u0195n\3\2\2\2\u0196\u0197\t\5\2")
        buf.write("\2\u0197p\3\2\2\2\u0198\u019b\5\35\17\2\u0199\u019b\5")
        buf.write("\r\7\2\u019a\u0198\3\2\2\2\u019a\u0199\3\2\2\2\u019br")
        buf.write("\3\2\2\2\u019c\u01a0\7$\2\2\u019d\u019f\5u;\2\u019e\u019d")
        buf.write("\3\2\2\2\u019f\u01a2\3\2\2\2\u01a0\u019e\3\2\2\2\u01a0")
        buf.write("\u01a1\3\2\2\2\u01a1\u01a3\3\2\2\2\u01a2\u01a0\3\2\2\2")
        buf.write("\u01a3\u01a4\7$\2\2\u01a4\u01a5\b:\5\2\u01a5t\3\2\2\2")
        buf.write("\u01a6\u01ab\n\b\2\2\u01a7\u01ab\5w<\2\u01a8\u01a9\7^")
        buf.write("\2\2\u01a9\u01ab\7$\2\2\u01aa\u01a6\3\2\2\2\u01aa\u01a7")
        buf.write("\3\2\2\2\u01aa\u01a8\3\2\2\2\u01abv\3\2\2\2\u01ac\u01ad")
        buf.write("\7^\2\2\u01ad\u01ae\t\t\2\2\u01aex\3\2\2\2\u01af\u01b0")
        buf.write("\7^\2\2\u01b0\u01b1\n\t\2\2\u01b1z\3\2\2\2\u01b2\u01b6")
        buf.write("\7$\2\2\u01b3\u01b5\5u;\2\u01b4\u01b3\3\2\2\2\u01b5\u01b8")
        buf.write("\3\2\2\2\u01b6\u01b4\3\2\2\2\u01b6\u01b7\3\2\2\2\u01b7")
        buf.write("\u01ba\3\2\2\2\u01b8\u01b6\3\2\2\2\u01b9\u01bb\t\n\2\2")
        buf.write("\u01ba\u01b9\3\2\2\2\u01bb\u01bc\3\2\2\2\u01bc\u01bd\b")
        buf.write(">\6\2\u01bd|\3\2\2\2\u01be\u01c2\7$\2\2\u01bf\u01c1\5")
        buf.write("u;\2\u01c0\u01bf\3\2\2\2\u01c1\u01c4\3\2\2\2\u01c2\u01c0")
        buf.write("\3\2\2\2\u01c2\u01c3\3\2\2\2\u01c3\u01c5\3\2\2\2\u01c4")
        buf.write("\u01c2\3\2\2\2\u01c5\u01c6\5y=\2\u01c6\u01c7\b?\7\2\u01c7")
        buf.write("~\3\2\2\2\u01c8\u01c9\7\61\2\2\u01c9\u01ca\7\61\2\2\u01ca")
        buf.write("\u01ce\3\2\2\2\u01cb\u01cd\n\13\2\2\u01cc\u01cb\3\2\2")
        buf.write("\2\u01cd\u01d0\3\2\2\2\u01ce\u01cc\3\2\2\2\u01ce\u01cf")
        buf.write("\3\2\2\2\u01cf\u01d1\3\2\2\2\u01d0\u01ce\3\2\2\2\u01d1")
        buf.write("\u01d2\b@\b\2\u01d2\u0080\3\2\2\2\u01d3\u01d4\7\61\2\2")
        buf.write("\u01d4\u01d5\7,\2\2\u01d5\u01d9\3\2\2\2\u01d6\u01d8\13")
        buf.write("\2\2\2\u01d7\u01d6\3\2\2\2\u01d8\u01db\3\2\2\2\u01d9\u01da")
        buf.write("\3\2\2\2\u01d9\u01d7\3\2\2\2\u01da\u01dc\3\2\2\2\u01db")
        buf.write("\u01d9\3\2\2\2\u01dc\u01dd\7,\2\2\u01dd\u01de\7\61\2\2")
        buf.write("\u01de\u01df\3\2\2\2\u01df\u01e0\bA\b\2\u01e0\u0082\3")
        buf.write("\2\2\2\u01e1\u01e3\t\f\2\2\u01e2\u01e1\3\2\2\2\u01e3\u01e4")
        buf.write("\3\2\2\2\u01e4\u01e2\3\2\2\2\u01e4\u01e5\3\2\2\2\u01e5")
        buf.write("\u01e6\3\2\2\2\u01e6\u01e7\bB\b\2\u01e7\u0084\3\2\2\2")
        buf.write("\u01e8\u01e9\13\2\2\2\u01e9\u01ea\bC\t\2\u01ea\u0086\3")
        buf.write("\2\2\2\34\2\u0141\u0149\u014d\u0152\u0156\u015a\u0161")
        buf.write("\u0165\u016a\u016e\u0172\u0179\u0180\u018a\u018f\u0194")
        buf.write("\u019a\u01a0\u01aa\u01b6\u01ba\u01c2\u01ce\u01d9\u01e4")
        buf.write("\n\3\62\2\3\63\3\3\64\4\3:\5\3>\6\3?\7\b\2\2\3C\b")
        return buf.getvalue()


class MT22Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    AUTO = 1
    BREAK = 2
    BOOLEAN = 3
    DO = 4
    ELSE = 5
    FALSE = 6
    FLOAT = 7
    FOR = 8
    FUNCTION = 9
    IF = 10
    INTEGER = 11
    RETURN = 12
    STRING = 13
    TRUE = 14
    WHILE = 15
    VOID = 16
    OUT = 17
    CONTINUE = 18
    OF = 19
    INHERIT = 20
    ARRAY = 21
    ADD = 22
    SUB = 23
    MUL = 24
    DIV = 25
    MOD = 26
    NOT = 27
    AND = 28
    OR = 29
    DEQ = 30
    NEQ = 31
    LT = 32
    LE = 33
    GT = 34
    GE = 35
    DC = 36
    LB = 37
    RB = 38
    LSB = 39
    RSB = 40
    DOT = 41
    CM = 42
    SM = 43
    CL = 44
    LP = 45
    RP = 46
    EQ = 47
    ID = 48
    INTLIT = 49
    POSINTLIT = 50
    FLOATLIT = 51
    BOOLEANLIT = 52
    STRINGLIT = 53
    UNCLOSE_STRING = 54
    ILLEGAL_ESCAPE = 55
    LINE_CMT = 56
    BLOCK_CMT = 57
    WS = 58
    ERROR_CHAR = 59

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'auto'", "'break'", "'boolean'", "'do'", "'else'", "'false'", 
            "'float'", "'for'", "'function'", "'if'", "'integer'", "'return'", 
            "'string'", "'true'", "'while'", "'void'", "'out'", "'continue'", 
            "'of'", "'inherit'", "'array'", "'+'", "'-'", "'*'", "'/'", 
            "'%'", "'!'", "'&&'", "'||'", "'=='", "'!='", "'<'", "'<='", 
            "'>'", "'>='", "'::'", "'('", "')'", "'['", "']'", "'.'", "','", 
            "';'", "':'", "'{'", "'}'", "'='" ]

    symbolicNames = [ "<INVALID>",
            "AUTO", "BREAK", "BOOLEAN", "DO", "ELSE", "FALSE", "FLOAT", 
            "FOR", "FUNCTION", "IF", "INTEGER", "RETURN", "STRING", "TRUE", 
            "WHILE", "VOID", "OUT", "CONTINUE", "OF", "INHERIT", "ARRAY", 
            "ADD", "SUB", "MUL", "DIV", "MOD", "NOT", "AND", "OR", "DEQ", 
            "NEQ", "LT", "LE", "GT", "GE", "DC", "LB", "RB", "LSB", "RSB", 
            "DOT", "CM", "SM", "CL", "LP", "RP", "EQ", "ID", "INTLIT", "POSINTLIT", 
            "FLOATLIT", "BOOLEANLIT", "STRINGLIT", "UNCLOSE_STRING", "ILLEGAL_ESCAPE", 
            "LINE_CMT", "BLOCK_CMT", "WS", "ERROR_CHAR" ]

    ruleNames = [ "AUTO", "BREAK", "BOOLEAN", "DO", "ELSE", "FALSE", "FLOAT", 
                  "FOR", "FUNCTION", "IF", "INTEGER", "RETURN", "STRING", 
                  "TRUE", "WHILE", "VOID", "OUT", "CONTINUE", "OF", "INHERIT", 
                  "ARRAY", "ADD", "SUB", "MUL", "DIV", "MOD", "NOT", "AND", 
                  "OR", "DEQ", "NEQ", "LT", "LE", "GT", "GE", "DC", "LB", 
                  "RB", "LSB", "RSB", "DOT", "CM", "SM", "CL", "LP", "RP", 
                  "EQ", "ID", "INTLIT", "POSINTLIT", "FLOATLIT", "INTEGERPART", 
                  "DECIMALPART", "EXPONENTPART", "DIGIT", "BOOLEANLIT", 
                  "STRINGLIT", "STRING_CHAR", "ESCAPE_SEQ", "ESC_ILLEGAL", 
                  "UNCLOSE_STRING", "ILLEGAL_ESCAPE", "LINE_CMT", "BLOCK_CMT", 
                  "WS", "ERROR_CHAR" ]

    grammarFileName = "MT22.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[48] = self.INTLIT_action 
            actions[49] = self.POSINTLIT_action 
            actions[50] = self.FLOATLIT_action 
            actions[56] = self.STRINGLIT_action 
            actions[60] = self.UNCLOSE_STRING_action 
            actions[61] = self.ILLEGAL_ESCAPE_action 
            actions[65] = self.ERROR_CHAR_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def INTLIT_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:
            self.text = self.text.replace("_", "")
     

    def POSINTLIT_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.text = self.text.replace("_", "")
     

    def FLOATLIT_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.text = self.text.replace("_", "")
     

    def STRINGLIT_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:

                s = str(self.text);
                self.text = s[1:-1]

     

    def UNCLOSE_STRING_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:

                        if self.text[-1] in ["\n","\r","\b","\t","\f"] :
                            raise UncloseString(self.text[1:-1])
                        else: raise UncloseString(self.text[1:])
                    
     

    def ILLEGAL_ESCAPE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 5:

                        raise IllegalEscape(self.text[1:])
                    
     

    def ERROR_CHAR_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 6:
            raise ErrorToken(self.text)
     


