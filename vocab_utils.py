import tensorflow as tf
import codecs
import os

UNK_ID=0
UNK="<unk>"
PAD="<pad>"

def check_vocab(vocab_file, out_dir, unk=None, pad=None):
    print (vocab_file)
    if tf.gfile.Exists(vocab_file):
        print(" Vocab file %s exists "% vocab_file)
        vocab= []
        with codecs.getreader("utf-8")(tf.gfile.GFile(vocab_file,"rb")) as f:
            vocab_size = 0
            for word in f:
                vocab_size+=1
                vocab.append(word.strip())

        if not unk: unk = UNK
        if not pad: pad = PAD
        assert len(vocab)>=2
        if vocab[0] != unk or vocab[1] != pad:
            print("The first 2 vocab words [%s, %s]"
                            " are not [%s, %s]" %
                            (vocab[0], vocab[1], unk, pad))
            vocab = [unk, pad] + vocab
            vocab_size += 3
            new_vocab_file = os.path.join(out_dir, os.path.basename(vocab_file))
            with codecs.getwriter("utf-8")(tf.gfile.GFile(new_vocab_file, "wb")) as f:
                newline = ''
                for word in vocab:
                    f.write(newline + "%s" % word)
                    newline = "\n"

            # save also a mapping file
            new_vocab_file_map = os.path.join(out_dir, "map_" + os.path.basename(vocab_file))
            with codecs.getwriter("utf-8")(tf.gfile.GFile(new_vocab_file_map, "wb")) as f:
                newline = ''
                for i, word in enumerate(vocab):
                    f.write(newline + "%d: %s" % (i, word))
                    newline = "\n"
            vocab_file = new_vocab_file
    else:
        raise ValueError("vocab_file does not exist.")

    vocab_size = len(vocab)
    return vocab_size, vocab_file

def create_vocab_table(vocab_file):
    return tf.contrib.lookup.index_table_from_file(vocab_file, default_value=UNK_ID)